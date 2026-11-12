import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

from broken import Controller, FakeBackend, PermanentError, TransientError


class Clock:
    def __init__(self):
        self.now = 100.0

    def __call__(self):
        return self.now


def make(desired, actual=None, script=None, **kwargs):
    clock = Clock()
    backend = FakeBackend(desired, actual, script)
    return Controller(backend, clock, **kwargs), backend, clock


def test_reconcile_creates_missing_resource():
    ctl, backend, _ = make({"web": {"replicas": 3}})
    ctl.enqueue("web")
    assert ctl.run_once() == [("web", "applied")]
    assert backend.actual["web"] == {"replicas": 3}


def test_reconcile_is_idempotent_when_state_already_matches():
    ctl, backend, _ = make({"web": {"replicas": 3}}, actual={"web": {"replicas": 3}})
    ctl.enqueue("web")
    assert ctl.run_once() == [("web", "noop")]
    assert backend.apply_calls == [], "converged resources must not be touched again"


def test_transient_error_is_requeued_with_exponential_backoff():
    boom = TransientError("throttled")
    ctl, backend, clock = make({"web": {"r": 1}}, script={"web": [boom, boom, boom]}, base_delay=1.0, max_delay=30.0)
    ctl.enqueue("web")
    delays = []
    for _ in range(3):
        assert ctl.run_once() == [("web", "requeued")]
        delays.append(ctl.queue["web"] - clock.now)
        clock.now = ctl.queue["web"]
    assert delays == [1.0, 2.0, 4.0]
    assert ctl.run_once() == [("web", "applied")]


def test_backoff_is_capped():
    boom = TransientError("slow")
    ctl, _, clock = make({"a": 1}, script={"a": [boom] * 8}, base_delay=1.0, max_delay=5.0)
    ctl.enqueue("a")
    delays = []
    for _ in range(6):
        ctl.run_once()
        delays.append(ctl.queue["a"] - clock.now)
        clock.now = ctl.queue["a"]
    assert delays == [1.0, 2.0, 4.0, 5.0, 5.0, 5.0]


def test_nothing_runs_before_the_requeue_delay_elapses():
    ctl, backend, clock = make({"a": 1}, script={"a": [TransientError("x")]})
    ctl.enqueue("a")
    ctl.run_once()
    clock.now += 0.5
    assert ctl.run_once() == []
    clock.now += 0.5
    assert ctl.run_once() == [("a", "applied")]


def test_permanent_error_is_recorded_and_never_retried():
    ctl, backend, clock = make({"a": 1}, script={"a": [PermanentError("quota policy forbids")]})
    ctl.enqueue("a")
    assert ctl.run_once() == [("a", "failed")]
    assert ctl.dead == {"a": "quota policy forbids"}
    assert "a" not in ctl.queue, "retrying a permanent failure only burns API quota"
    clock.now += 1000
    assert ctl.run_once() == []


def test_success_resets_the_failure_streak():
    boom = TransientError("flap")
    ctl, backend, clock = make({"a": 1}, script={"a": [boom, boom]}, base_delay=1.0)
    ctl.enqueue("a")
    for _ in range(3):
        ctl.run_once()
        if "a" in ctl.queue:
            clock.now = ctl.queue["a"]
    assert "a" not in ctl.failures
    backend.actual.pop("a")
    backend.script["a"] = [TransientError("again")]
    ctl.enqueue("a")
    ctl.run_once()
    assert ctl.queue["a"] - clock.now == 1.0, "a new incident starts from the base delay again"


def test_duplicate_enqueues_collapse_and_keys_run_in_order():
    ctl, backend, clock = make({"b": 1, "a": 2})
    ctl.enqueue("b")
    ctl.enqueue("a")
    ctl.enqueue("b")
    assert ctl.run_once() == [("a", "applied"), ("b", "applied")]
    assert backend.apply_calls == ["a", "b"]
