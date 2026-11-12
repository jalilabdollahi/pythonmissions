import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import broken


class Clock:
    def __init__(self):
        self.now = 1000.0

    def __call__(self):
        return self.now


def make(window=60):
    clock = Clock()
    return broken.SlidingWindowCounter(window, clock), clock


def test_counts_recent_hits():
    counter, clock = make()
    for _ in range(3):
        counter.hit("k1")
        clock.now += 1
    assert counter.count("k1") == 3
    assert counter.count("other") == 0


def test_idle_key_count_drops_without_new_hits():
    counter, clock = make()
    counter.hit("k1")
    clock.now += 61
    assert counter.count("k1") == 0, "count must evict stale timestamps itself"


def test_request_exactly_one_window_old_is_outside():
    counter, clock = make(60)
    counter.hit("k1")
    clock.now += 60
    assert counter.count("k1") == 0


def test_request_just_inside_window_is_counted():
    counter, clock = make(60)
    counter.hit("k1")
    clock.now += 59.9
    assert counter.count("k1") == 1


def test_allow_enforces_limit():
    counter, clock = make()
    results = [counter.allow("k1", 3) for _ in range(5)]
    assert results == [True, True, True, False, False]


def test_rejected_requests_are_not_recorded():
    counter, clock = make(60)
    for _ in range(5):
        counter.allow("k1", 2)
    assert counter.count("k1") == 2, "only accepted requests count against the limit"
    clock.now += 60
    assert counter.allow("k1", 2) is True


def test_busiest_keys_ignore_stale_entries():
    counter, clock = make()
    for _ in range(4):
        counter.hit("old")
    clock.now += 100
    counter.hit("new")
    assert counter.busiest() == [("new", 1)]
