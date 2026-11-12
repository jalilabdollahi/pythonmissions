import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import broken


class Clock:
    def __init__(self):
        self.now = 100.0

    def __call__(self):
        return self.now


def make(capacity=5, rate=2.0):
    clock = Clock()
    return broken.TokenBucket(capacity, rate, clock), clock


def test_starts_full_and_allows_a_burst():
    bucket, _ = make()
    assert broken.burst_size(bucket) == 5


def test_rejects_when_empty_without_changing_state():
    bucket, clock = make(capacity=2)
    assert bucket.allow() and bucket.allow()
    assert bucket.allow() is False
    clock.now += 0.5
    assert bucket.allow() is True, "0.5s * 2 tokens/s = exactly 1 token, which is enough"


def test_refills_at_the_configured_rate():
    bucket, clock = make(capacity=10, rate=2.0)
    for _ in range(10):
        bucket.allow()
    clock.now += 3
    assert broken.burst_size(bucket) == 6


def test_idle_bucket_never_exceeds_capacity():
    bucket, clock = make(capacity=5, rate=2.0)
    clock.now += 10_000
    assert broken.burst_size(bucket) == 5, "tokens must be capped at capacity"


def test_elapsed_time_is_counted_only_once():
    bucket, clock = make(capacity=10, rate=1.0)
    for _ in range(10):
        bucket.allow()
    clock.now += 2
    assert bucket.allow()  # refill adds 2, spend 1 -> 1 left
    assert bucket.allow()  # same instant: nothing new may appear
    assert bucket.allow() is False, "advance the last-refill time each time you refill"


def test_cost_larger_than_one():
    bucket, _ = make(capacity=5)
    assert bucket.allow(cost=5) is True
    assert bucket.allow(cost=1) is False


def test_retry_after():
    bucket, clock = make(capacity=2, rate=2.0)
    bucket.allow(2)
    assert bucket.retry_after(1) == 0.5
    clock.now += 0.25
    assert bucket.retry_after(1) == 0.25
    assert bucket.retry_after(0) == 0.0
