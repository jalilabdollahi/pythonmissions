import asyncio
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

from broken import SlotPool, render_all


def drive(coro, timeout=2):
    return asyncio.run(asyncio.wait_for(coro, timeout))


async def settle(times=5):
    for _ in range(times):
        await asyncio.sleep(0)


def test_capacity_is_respected_and_slots_return():
    async def scenario():
        pool = SlotPool(2)
        gate = asyncio.Event()
        running = 0
        peak = 0

        async def job():
            nonlocal running, peak
            running += 1
            peak = max(peak, running)
            await gate.wait()
            running -= 1
            return "ok"

        tasks = [asyncio.ensure_future(pool.run(job)) for _ in range(5)]
        await settle()
        assert peak == 2 and pool.waiting() == 3
        gate.set()
        assert await asyncio.gather(*tasks) == ["ok"] * 5
        assert pool.in_use == 0

    drive(scenario())


def test_failed_job_releases_its_slot():
    async def scenario():
        pool = SlotPool(1)

        async def boom():
            raise RuntimeError("renderer crashed")

        results = await render_all(pool, [boom, boom])
        assert all(isinstance(r, RuntimeError) for r in results)
        assert pool.in_use == 0

    drive(scenario())


def test_cancelling_a_running_job_releases_its_slot():
    async def scenario():
        pool = SlotPool(1)
        started = asyncio.Event()

        async def slow():
            started.set()
            await asyncio.Event().wait()

        task = asyncio.ensure_future(pool.run(slow))
        await started.wait()
        task.cancel()
        with pytest.raises(asyncio.CancelledError):
            await task
        assert pool.in_use == 0, "CancelledError is a BaseException: it must still free the slot"

        async def quick():
            return "after"

        assert await pool.run(quick) == "after"

    drive(scenario())


def test_cancelling_a_waiter_does_not_consume_or_free_a_slot():
    async def scenario():
        pool = SlotPool(1)
        gate = asyncio.Event()

        async def hold():
            await gate.wait()

        async def never():
            raise AssertionError("cancelled waiter must not run")

        holder = asyncio.ensure_future(pool.run(hold))
        await settle()
        waiter = asyncio.ensure_future(pool.run(never))
        await settle()
        waiter.cancel()
        with pytest.raises(asyncio.CancelledError):
            await waiter
        assert pool.in_use == 1, "the waiter never owned a slot, so nothing may be released"
        assert pool.waiting() == 0
        gate.set()
        await holder
        assert pool.in_use == 0

    drive(scenario())


def test_release_skips_waiters_that_were_cancelled_in_the_same_tick():
    async def scenario():
        pool = SlotPool(1)
        await pool.acquire()
        order = []

        async def want(name):
            await pool.acquire()
            order.append(name)

        doomed = asyncio.ensure_future(want("doomed"))
        survivor = asyncio.ensure_future(want("survivor"))
        await settle()
        doomed.cancel()
        pool.release()  # runs before the doomed task had a chance to handle its cancellation
        await asyncio.wait_for(survivor, 1)
        assert order == ["survivor"], "the slot must go to the next live waiter, not a dead one"
        assert pool.in_use == 1

    drive(scenario())


def test_slot_handed_to_a_waiter_cancelled_in_the_same_tick_is_not_lost():
    async def scenario():
        pool = SlotPool(1)
        await pool.acquire()

        async def want():
            await pool.acquire()

        waiter = asyncio.ensure_future(want())
        await settle()
        pool.release()  # hands the slot directly to the waiter's future
        waiter.cancel()  # but the waiter is cancelled before it resumes
        with pytest.raises(asyncio.CancelledError):
            await waiter
        assert pool.in_use == 0, "a slot handed to a cancelled waiter must be given back"
        await asyncio.wait_for(pool.acquire(), 1)

    drive(scenario())


def test_grow_hands_new_capacity_to_waiters_and_try_acquire_is_non_blocking():
    async def scenario():
        pool = SlotPool(1)
        assert pool.try_acquire() is True
        assert pool.try_acquire() is False
        got = []

        async def want(name):
            await pool.acquire()
            got.append(name)

        tasks = [asyncio.ensure_future(want(n)) for n in "ab"]
        await settle()
        pool.grow(1)
        await settle()
        assert got == ["a"], "one extra slot serves exactly one waiter"
        assert pool.stats() == {"capacity": 2, "in_use": 2, "waiting": 1}
        pool.release()
        await asyncio.gather(*tasks)
        assert got == ["a", "b"]

    drive(scenario())
