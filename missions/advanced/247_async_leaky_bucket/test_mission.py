import asyncio
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

from broken import LeakyBucket, TenantThrottle


class FakeTime:
    def __init__(self):
        self.now = 1000.0
        self.sleeps = []

    def __call__(self):
        return self.now

    async def sleep(self, seconds):
        self.sleeps.append(seconds)
        self.now += seconds
        await asyncio.sleep(0)


def drive(coro, timeout=2):
    return asyncio.run(asyncio.wait_for(coro, timeout))


def test_bucket_absorbs_a_burst_up_to_capacity_then_waits():
    async def scenario():
        t = FakeTime()
        bucket = LeakyBucket(10, 2.0, t, t.sleep)
        for _ in range(10):
            await bucket.acquire()
        assert t.sleeps == [], "a full burst fits without waiting"
        await bucket.acquire()
        assert t.sleeps == [0.5], "one more unit needs 1/2 second of leaking"

    drive(scenario())


def test_exact_fit_does_not_wait():
    async def scenario():
        t = FakeTime()
        bucket = LeakyBucket(10, 2.0, t, t.sleep)
        await bucket.acquire(9)
        await bucket.acquire(1)
        assert t.sleeps == [], "level + cost == capacity is allowed"
        assert bucket.level == 10

    drive(scenario())


def test_idle_time_does_not_bank_unlimited_credit():
    async def scenario():
        t = FakeTime()
        bucket = LeakyBucket(10, 2.0, t, t.sleep)
        await bucket.acquire(4)
        t.now += 3600
        for _ in range(10):
            await bucket.acquire()
        assert t.sleeps == []
        await bucket.acquire()
        assert t.sleeps == [0.5], "after an hour idle the bucket is empty, not negative"

    drive(scenario())


def test_leak_is_measured_from_the_last_update_only_once():
    async def scenario():
        t = FakeTime()
        bucket = LeakyBucket(10, 1.0, t, t.sleep)
        await bucket.acquire(10)
        t.now += 4
        await bucket.acquire(1)
        assert bucket.level == pytest.approx(7.0)
        await bucket.acquire(1)
        assert bucket.level == pytest.approx(8.0), "elapsed time must not be drained twice"

    drive(scenario())


def test_try_acquire_refusal_does_not_consume_capacity():
    t = FakeTime()
    bucket = LeakyBucket(5, 1.0, t, t.sleep)
    assert bucket.try_acquire(4) is True
    assert bucket.try_acquire(2) is False
    assert bucket.level == 4, "a refused request must leave the bucket unchanged"
    assert bucket.retry_after(2) == pytest.approx(1.0)
    assert bucket.try_acquire(1) is True


def test_cost_larger_than_capacity_is_rejected():
    async def scenario():
        bucket = LeakyBucket(5, 1.0, FakeTime(), FakeTime().sleep)
        with pytest.raises(ValueError):
            await bucket.acquire(6)
        with pytest.raises(ValueError):
            await bucket.acquire(0)

    drive(scenario())


def test_waiters_are_served_in_arrival_order():
    async def scenario():
        t = FakeTime()
        bucket = LeakyBucket(5, 5.0, t, t.sleep)
        await bucket.acquire(5)
        order = []

        async def want(name):
            await bucket.acquire(5)
            order.append(name)

        await asyncio.gather(want("a"), want("b"), want("c"))
        assert order == ["a", "b", "c"]
        assert t.now == pytest.approx(1000.0 + 3.0)

    drive(scenario())


def test_tenants_are_throttled_independently():
    async def scenario():
        t = FakeTime()
        throttle = TenantThrottle(1, 1.0, t, t.sleep)
        sent = []

        async def deliver(tenant, message):
            sent.append((tenant, message))
            return True

        await throttle.send("acme", deliver, "hi")
        await throttle.send("globex", deliver, "hi")
        assert t.sleeps == [], "globex must not pay for acme's traffic"
        await throttle.send("acme", deliver, "again")
        assert t.sleeps == [1.0]
        assert len(sent) == 3

    drive(scenario())
