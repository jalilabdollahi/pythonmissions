import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import broken


import sys
import threading


def hammer(stats, threads=8, per_thread=4000):
    barrier = threading.Barrier(threads)

    def work():
        barrier.wait()
        for _ in range(per_thread):
            stats.record("/up", 3)

    pool = [threading.Thread(target=work) for _ in range(threads)]
    for t in pool:
        t.start()
    for t in pool:
        t.join()


@pytest.fixture
def fast_switching():
    old = sys.getswitchinterval()
    sys.setswitchinterval(1e-6)
    yield
    sys.setswitchinterval(old)


def test_single_threaded_recording():
    stats = broken.UploadStats()
    stats.record("/a", 10)
    stats.record("/a", 5)
    stats.record("/b", 1)
    assert stats.snapshot() == {"count": 3, "bytes": 16, "by_route": {"/a": 2, "/b": 1}}


def test_concurrent_records_lose_no_updates(fast_switching):
    stats = broken.UploadStats()
    hammer(stats)
    snap = stats.snapshot()
    assert snap["count"] == 32000, "all threads must share one lock around the read-modify-write"
    assert snap["bytes"] == 96000
    assert snap["by_route"] == {"/up": 32000}


def test_record_batch_can_call_record_without_deadlocking():
    stats = broken.UploadStats()
    t = threading.Thread(target=stats.record_batch, args=("/b", [1, 2, 3]), daemon=True)
    t.start()
    t.join(timeout=0.5)
    assert not t.is_alive(), "a thread holding a plain Lock blocks itself; use a re-entrant lock"
    assert stats.snapshot()["count"] == 3


def test_snapshot_is_a_copy_not_the_live_dict():
    stats = broken.UploadStats()
    stats.record("/a", 1)
    snap = stats.snapshot()
    stats.record("/a", 1)
    stats.record("/z", 1)
    assert snap["by_route"] == {"/a": 1}, "later uploads must not change an earlier snapshot"
