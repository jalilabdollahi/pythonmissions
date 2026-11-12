import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import broken


import asyncio


class Tracker:
    def __init__(self, fail=()):
        self.active = 0
        self.peak = 0
        self.fail = set(fail)

    async def fetch(self, url):
        self.active += 1
        self.peak = max(self.peak, self.active)
        try:
            for _ in range(3):
                await asyncio.sleep(0)
            if url in self.fail:
                raise LookupError("404 " + url)
            return url.upper()
        finally:
            self.active -= 1


def run(coro, timeout=1.0):
    async def guarded():
        return await asyncio.wait_for(coro, timeout)
    return asyncio.run(guarded())


def test_results_follow_url_order():
    t = Tracker()
    out = run(broken.fetch_all(["a", "b", "c", "d"], t.fetch, limit=2))
    assert out == ["A", "B", "C", "D"]


def test_never_more_than_limit_in_flight():
    t = Tracker()
    run(broken.fetch_all(["u%d" % i for i in range(10)], t.fetch, limit=3))
    assert t.peak == 3, "all tasks must share one semaphore (peak was %d)" % t.peak


def test_limit_one_serialises_everything():
    t = Tracker()
    run(broken.fetch_all(["a", "b", "c"], t.fetch, limit=1))
    assert t.peak == 1


def test_failure_is_returned_and_does_not_leak_a_slot():
    t = Tracker(fail=["bad"])
    out = run(broken.fetch_all(["a", "bad", "c", "d"], t.fetch, limit=1))
    assert out[0] == "A" and out[2] == "C" and out[3] == "D", "a failed fetch must release its permit"
    assert isinstance(out[1], LookupError)


def test_limit_below_one_is_rejected_immediately():
    t = Tracker()
    with pytest.raises(ValueError) as info:
        run(broken.fetch_all(["a"], t.fetch, limit=0), timeout=0.3)
    assert "at least 1" in str(info.value)


def test_split_results():
    err = ValueError("x")
    assert broken.split_results(["a", err, "b"]) == (["a", "b"], [err])
    assert broken.split_results([]) == ([], [])
