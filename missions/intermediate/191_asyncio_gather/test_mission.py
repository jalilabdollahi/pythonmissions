import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import broken


import asyncio


def make_probe(statuses, rendezvous=None):
    started = []
    gate = {}

    async def probe(name):
        if rendezvous:
            started.append(name)
            if len(started) == rendezvous:
                gate["ev"].set()
            await asyncio.wait_for(gate["ev"].wait(), timeout=0.2)
        value = statuses[name]
        if isinstance(value, Exception):
            raise value
        return value

    def arm():
        gate["ev"] = asyncio.Event()

    probe.arm = arm
    return probe


def run(names, probe):
    async def main():
        probe.arm()
        return await broken.check_all(names, probe)
    return asyncio.run(main())


def test_check_service_returns_the_awaited_status():
    async def probe(name):
        return "ok"

    assert asyncio.run(broken.check_service("api", probe)) == "ok", "probe(...) is a coroutine: await it"


def test_report_maps_names_to_statuses_in_order():
    probe = make_probe({"a": "ok", "b": "slow", "c": "ok"})
    report = run(["c", "a", "b"], probe)
    assert list(report.items()) == [("c", "ok"), ("a", "ok"), ("b", "slow")]


def test_checks_run_concurrently():
    names = ["s1", "s2", "s3", "s4"]
    probe = make_probe({n: "ok" for n in names}, rendezvous=len(names))
    report = run(names, probe)
    assert report == {n: "ok" for n in names}, "every probe waits for all others to start: awaiting one by one cannot work"


def test_one_failing_probe_does_not_hide_the_others():
    probe = make_probe({"a": "ok", "b": ConnectionError("down"), "c": "ok"})
    report = run(["a", "b", "c"], probe)
    assert report == {"a": "ok", "b": "error: ConnectionError", "c": "ok"}


def test_count_ok():
    assert broken.count_ok({"a": "ok", "b": "error: X", "c": "ok"}) == 2
    assert broken.count_ok({}) == 0


def test_empty_names():
    probe = make_probe({})
    assert run([], probe) == {}
