import pytest, sys, threading
sys.path.insert(0, ".")
from broken import ObjectPool, PooledMetric

def test_acquire_release():
    pool = ObjectPool(PooledMetric, size=5)
    obj = pool.acquire()
    assert isinstance(obj, PooledMetric)
    pool.release(obj)

def test_exhausted_creates_new():
    pool = ObjectPool(PooledMetric, size=1)
    obj1 = pool.acquire()
    obj2 = pool.acquire()  # should create new, not raise
    assert obj2 is not None
    assert obj1 is not obj2

def test_reset_on_release():
    pool = ObjectPool(PooledMetric, size=5)
    obj = pool.acquire()
    obj.name = "cpu"
    obj.value = 99.9
    pool.release(obj)
    obj2 = pool.acquire()
    assert obj2.name == ""
    assert obj2.value == 0.0
