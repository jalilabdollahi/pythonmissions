import asyncio
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

from broken import format_report, preflight, run_fail_fast, run_settled, summarize


def drive(coro, timeout=3):
    return asyncio.run(asyncio.wait_for(coro, timeout))


async def ticks(n):
    for _ in range(n):
        await asyncio.sleep(0)


def make_slow(log, name):
    async def slow():
        try:
            await asyncio.Event().wait()
        finally:
            await ticks(2)  # async cleanup that needs the loop to finish
            log.append(f"{name} cleaned")

    return slow


def test_results_come_back_in_submission_order():
    async def scenario():
        async def late():
            await ticks(5)
            return "late"

        async def early():
            return "early"

        assert await run_fail_fast([late, early]) == ["late", "early"]

    drive(scenario())


def test_first_failure_is_raised_even_if_another_check_finished_first():
    async def scenario():
        log = []

        async def quick_ok():
            return "ok"

        async def fails_later():
            await ticks(3)
            raise RuntimeError("disk full")

        with pytest.raises(RuntimeError, match="disk full"):
            await run_fail_fast([quick_ok, fails_later, make_slow(log, "slow")])

    drive(scenario())


def test_siblings_are_cancelled_and_finished_unwinding_before_returning():
    async def scenario():
        log = []

        async def boom():
            await ticks(2)
            raise ValueError("bad config")

        with pytest.raises(ValueError):
            await run_fail_fast([make_slow(log, "a"), boom, make_slow(log, "b")])
        assert sorted(log) == ["a cleaned", "b cleaned"], "cleanup must be awaited, not just requested"
        leftover = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
        assert leftover == []

    drive(scenario())


def test_timeout_cancels_everything_still_running():
    async def scenario():
        log = []
        with pytest.raises(asyncio.TimeoutError):
            await run_fail_fast([make_slow(log, "x"), make_slow(log, "y")], timeout=0.05)
        assert sorted(log) == ["x cleaned", "y cleaned"]

    drive(scenario())


def test_cancelling_the_caller_cancels_the_children():
    async def scenario():
        log = []
        runner = asyncio.ensure_future(run_fail_fast([make_slow(log, "child")]))
        await ticks(3)
        runner.cancel()
        done, _ = await asyncio.wait({runner}, timeout=1)
        assert done, "a cancelled caller must cancel its children, otherwise it waits for them forever"
        assert runner.cancelled()
        assert log == ["child cleaned"], "children must not outlive a cancelled parent"

    drive(scenario())


def test_settled_reports_every_outcome_including_cancelled_checks():
    async def scenario():
        async def ok():
            return 42

        async def bad():
            raise ValueError("nope")

        async def cancelled():
            raise asyncio.CancelledError()

        outcomes = await run_settled({"ok": ok, "bad": bad, "cancelled": cancelled})
        flags = {o.name: o.ok for o in outcomes}
        assert flags == {"ok": True, "bad": False, "cancelled": False}, (
            "return_exceptions=True also returns CancelledError objects, which are not Exception"
        )
        assert format_report(outcomes) == "PASS ok: 42\nFAIL bad: ValueError\nFAIL cancelled: CancelledError"
        assert summarize(outcomes) == {"passed": 1, "failed": ["bad", "cancelled"], "healthy": False}

    drive(scenario())


def test_preflight_modes():
    async def scenario():
        async def ok():
            return "fine"

        async def bad():
            raise OSError("unreachable")

        assert await preflight({"a": ok, "b": ok}) == ["fine", "fine"]
        assert await preflight({"a": ok, "b": ok}, fail_fast=False) == {"passed": 2, "failed": [], "healthy": True}
        with pytest.raises(OSError):
            await preflight({"a": ok, "b": bad})
        report = await preflight({"a": ok, "b": bad}, fail_fast=False)
        assert report["failed"] == ["b"]

    drive(scenario())
