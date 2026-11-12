import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import broken


import asyncio


def make_probe():
    never = {}

    async def probe(name):
        if name.startswith("hang"):
            await asyncio.Event().wait()
        if name.startswith("bad"):
            raise ConnectionResetError("reset")
        return "200 " + name

    return probe


def run(coro, outer=1.5):
    async def guarded():
        return await asyncio.wait_for(coro, outer)
    return asyncio.run(guarded())


def test_fast_probe_is_ok():
    out = run(broken.run_probe("api", make_probe(), 50))
    assert out == {"name": "api", "status": "ok", "value": "200 api"}


def test_hung_probe_times_out_after_milliseconds_not_seconds():
    out = run(broken.run_probe("hang1", make_probe(), 20))
    assert out == {"name": "hang1", "status": "timeout", "value": None}, "wait_for takes seconds: convert from ms"


def test_failing_probe_reports_error_class():
    out = run(broken.run_probe("bad1", make_probe(), 50))
    assert out == {"name": "bad1", "status": "error", "value": "ConnectionResetError"}


def test_each_probe_has_its_own_deadline():
    results = run(broken.run_all(["ok1", "hang1", "ok2"], make_probe(), timeout_ms=20))
    assert [r["status"] for r in results] == ["ok", "timeout", "ok"], "one hung probe must not fail the batch"
    assert [r["name"] for r in results] == ["ok1", "hang1", "ok2"]


def test_worst_orders_by_severity_not_alphabetically():
    def res(*statuses):
        return [{"name": "x", "status": s, "value": None} for s in statuses]

    assert broken.worst(res("ok", "timeout")) == "timeout"
    assert broken.worst(res("timeout", "error", "ok")) == "error", "error is worse than timeout"
    assert broken.worst(res("ok", "ok")) == "ok"
    assert broken.worst([]) == "ok"
