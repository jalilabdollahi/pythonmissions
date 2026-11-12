import asyncio
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

from broken import DeliveryPipeline, from_list


def drive(coro, timeout=2):
    return asyncio.run(asyncio.wait_for(coro, timeout))


async def echo(item):
    await asyncio.sleep(0)
    return item


def test_delivers_everything_and_finishes():
    async def scenario():
        pipe = DeliveryPipeline(echo, workers=3, maxsize=2)
        report = await pipe.run(from_list(range(10)))
        assert sorted(report.delivered) == list(range(10))
        assert report.summary() == {"delivered": 10, "failed": 0}

    drive(scenario())


def test_every_worker_receives_its_own_stop_signal():
    async def scenario():
        pipe = DeliveryPipeline(echo, workers=4, maxsize=2)
        await pipe.run(from_list(range(3)))
        assert all(t.done() and not t.cancelled() for t in pipe.active_tasks), (
            "workers must exit by themselves; one sentinel is needed per worker"
        )

    drive(scenario())


def test_a_failing_delivery_is_recorded_and_the_worker_keeps_going():
    async def scenario():
        async def flaky(item):
            await asyncio.sleep(0)
            if item % 2:
                raise ConnectionError("endpoint down")
            return item

        pipe = DeliveryPipeline(flaky, workers=1, maxsize=2)
        report = await pipe.run(from_list(range(6)))
        assert report.delivered == [0, 2, 4], "one bad webhook must not kill the only worker"
        assert report.failed == [(1, "ConnectionError"), (3, "ConnectionError"), (5, "ConnectionError")]

    drive(scenario())


def test_empty_source_shuts_down_immediately():
    async def scenario():
        pipe = DeliveryPipeline(echo, workers=2)
        report = await pipe.run(from_list([]))
        assert report.summary() == {"delivered": 0, "failed": 0}

    drive(scenario())


def test_queue_is_drained_before_shutdown():
    async def scenario():
        release = asyncio.Event()

        async def slow(item):
            await release.wait()
            return item

        pipe = DeliveryPipeline(slow, workers=2, maxsize=3)
        runner = asyncio.ensure_future(pipe.run(from_list(range(5))))
        for _ in range(10):
            await asyncio.sleep(0)
        assert not runner.done()
        release.set()
        report = await runner
        assert sorted(report.delivered) == [0, 1, 2, 3, 4], "items already queued must still be delivered"

    drive(scenario())


def test_source_failure_still_drains_queue_and_stops_workers():
    async def scenario():
        async def broken_source():
            for i in range(3):
                yield i
            raise RuntimeError("upstream disconnected")

        pipe = DeliveryPipeline(echo, workers=2, maxsize=5)
        with pytest.raises(RuntimeError, match="upstream"):
            await pipe.run(broken_source())
        assert sorted(pipe.report.delivered) == [0, 1, 2]
        assert all(t.done() and not t.cancelled() for t in pipe.active_tasks)

    drive(scenario())
