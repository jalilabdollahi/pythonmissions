import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import broken


class Clock:
    def __init__(self):
        self.now = 0.0

    def __call__(self):
        return self.now


def ok():
    return "fine"


def boom():
    raise ConnectionError("vendor down")


def attempt(breaker, fn):
    try:
        return breaker.call(fn)
    except ConnectionError:
        return "failed"


def make(threshold=3, timeout=30):
    clock = Clock()
    return broken.CircuitBreaker(threshold, timeout, clock), clock


def test_closed_breaker_passes_results_through():
    breaker, _ = make()
    assert breaker.call(ok) == "fine"
    assert breaker.state == "closed"


def test_exceptions_from_the_wrapped_call_are_reraised():
    breaker, _ = make()
    with pytest.raises(ConnectionError):
        breaker.call(boom)


def test_opens_after_threshold_consecutive_failures():
    breaker, _ = make(threshold=3)
    for _ in range(3):
        attempt(breaker, boom)
    assert breaker.state == "open"
    with pytest.raises(broken.CircuitOpenError):
        breaker.call(ok)


def test_success_resets_the_failure_count():
    breaker, _ = make(threshold=3)
    for fn in (boom, boom, ok, boom, boom):
        attempt(breaker, fn)
    assert breaker.state == "closed", "only consecutive failures count"


def test_open_breaker_does_not_run_the_function():
    breaker, _ = make(threshold=1)
    attempt(breaker, boom)
    calls = []
    with pytest.raises(broken.CircuitOpenError):
        breaker.call(lambda: calls.append(1))
    assert calls == []


def test_half_open_after_exactly_reset_timeout_and_success_closes():
    breaker, clock = make(threshold=1, timeout=30)
    attempt(breaker, boom)
    clock.now = 29.9
    with pytest.raises(broken.CircuitOpenError):
        breaker.call(ok)
    clock.now = 30.0
    assert breaker.call(ok) == "fine", "30s have passed, which is exactly the reset timeout"
    assert breaker.state == "closed"


def test_failed_half_open_trial_reopens_immediately():
    breaker, clock = make(threshold=3, timeout=10)
    for _ in range(3):
        attempt(breaker, boom)
    clock.now = 10
    assert attempt(breaker, boom) == "failed"
    assert breaker.state == "open", "one failed probe must reopen the breaker"
    with pytest.raises(broken.CircuitOpenError):
        breaker.call(ok)
    clock.now = 19.9
    with pytest.raises(broken.CircuitOpenError):
        breaker.call(ok)
