import pytest, sys, time
sys.path.insert(0, ".")
from broken import SlidingWindow

def test_count_recent():
    sw = SlidingWindow(window_seconds=60)
    sw.record()
    sw.record()
    sw.record()
    assert sw.count() == 3

def test_evicts_old():
    sw = SlidingWindow(window_seconds=0.05)
    sw.record()
    sw.record()
    time.sleep(0.1)
    assert sw.count() == 0

def test_mixed():
    sw = SlidingWindow(window_seconds=0.2)
    sw.record()
    time.sleep(0.15)
    sw.record()
    time.sleep(0.1)
    assert sw.count() == 1
