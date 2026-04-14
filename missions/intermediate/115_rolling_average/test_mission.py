import pytest, sys
sys.path.insert(0, ".")
from broken import RollingAverage

def test_average():
    r = RollingAverage(3)
    r.add(10)
    r.add(20)
    r.add(30)
    assert r.average() == 20.0

def test_window_size():
    r = RollingAverage(3)
    for i in range(10):
        r.add(i)
    assert r.count() == 3

def test_empty():
    r = RollingAverage(5)
    assert r.average() == 0.0
