import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import AgingQueue, drain


class Clock:
    def __init__(self):
        self.now = 0.0

    def __call__(self):
        return self.now


def make(rate=1.0, boost=100.0):
    clock = Clock()
    return clock, AgingQueue(clock, aging_rate=rate, max_boost=boost)


def test_without_waiting_lower_number_runs_first_and_equal_priority_is_fifo():
    clock, q = make()
    for name, prio in [("lint", 5), ("deploy", 1), ("test-a", 3), ("test-b", 3)]:
        q.push(name, prio)
    assert drain(q) == ["deploy", "test-a", "test-b", "lint"]


def test_waiting_jobs_age_past_newer_more_urgent_ones():
    clock, q = make(rate=1.0)
    q.push("nightly-report", 10)
    clock.now = 6.0
    q.push("hotfix", 5)
    assert q.peek() == "nightly-report", "10 - 6s of waiting = 4, which beats a fresh priority 5"
    assert q.ranking() == [("nightly-report", 4.0), ("hotfix", 5.0)]


def test_aging_is_capped_so_it_cannot_overtake_critical_work():
    clock, q = make(rate=1.0, boost=3.0)
    q.push("batch", 10)
    clock.now = 1000.0
    q.push("critical", 5)
    assert q.peek() == "critical", "a batch job may gain at most max_boost, so 10 - 3 = 7 is still behind 5"


def test_ties_go_to_the_job_that_arrived_first():
    clock, q = make(rate=1.0)
    q.push("older", 3)
    clock.now = 1.0
    q.push("newer", 2)
    assert dict(q.ranking()) == {"older": 2.0, "newer": 2.0}
    assert drain(q) == ["older", "newer"], "equal effective priority is decided by arrival order"


def test_requeued_job_keeps_its_age():
    clock, q = make(rate=1.0)
    q.push("flaky-build", 8)
    job = q.pop()
    clock.now = 4.0
    q.requeue(job)
    q.push("fresh", 5)
    assert job.attempts == 1
    assert q.peek() == "flaky-build", "8 - 4s of accumulated age = 4 beats a fresh 5; a retry must not lose its wait"


def test_delayed_jobs_are_invisible_until_their_time():
    clock, q = make()
    q.push("backoff-retry", 1, delay=30.0)
    q.push("normal", 9)
    assert q.peek() == "normal"
    assert drain(q) == ["normal"]
    assert len(q) == 1 and q.pop() is None
    clock.now = 30.0
    assert q.pop().id == "backoff-retry"


def test_cancel_removes_only_the_named_job():
    clock, q = make()
    q.push("a", 1)
    q.push("b", 2)
    assert q.cancel("a") is True
    assert q.cancel("a") is False
    assert drain(q) == ["b"]
