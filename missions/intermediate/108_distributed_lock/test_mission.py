import pytest, sys
sys.path.insert(0, ".")
from broken import DistributedLock

def test_acquire_and_release():
    lock = DistributedLock("test")
    assert lock.acquire("service-a")
    assert lock.is_locked()
    assert lock.release("service-a")
    assert not lock.is_locked()

def test_cannot_steal_lock():
    lock = DistributedLock("test", ttl=60)
    lock.acquire("service-a")
    assert not lock.release("service-b")
    assert lock.is_locked()

def test_expired_lock_can_be_acquired():
    lock = DistributedLock("test", ttl=0.01)
    lock.acquire("service-a")
    import time; time.sleep(0.05)
    assert lock.acquire("service-b", timeout=0.1)
