import os
import sys
import threading
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

from broken import ConnectionPool, PoolTimeout


class FakeConn:
    counter = 0

    def __init__(self):
        FakeConn.counter += 1
        self.name = f"conn-{FakeConn.counter}"
        self.closed = False

    def close(self):
        self.closed = True


def wait_until(predicate, limit=2.0):
    end = time.monotonic() + limit
    while time.monotonic() < end:
        if predicate():
            return True
        time.sleep(0.002)
    return False


def test_pool_never_creates_more_than_max_size():
    pool = ConnectionPool(FakeConn, 2)
    a, b = pool.acquire(), pool.acquire()
    assert a is not b
    with pytest.raises(PoolTimeout):
        pool.acquire(timeout=0.05)
    assert pool.stats()["created"] == 2


def test_released_connection_is_reused():
    pool = ConnectionPool(FakeConn, 2)
    a = pool.acquire()
    pool.release(a)
    assert pool.acquire() is a
    assert pool.stats() == {"idle": 0, "in_use": 1, "created": 1}


def test_release_wakes_a_blocked_waiter():
    pool = ConnectionPool(FakeConn, 1)
    held = pool.acquire()
    got = []
    worker = threading.Thread(target=lambda: got.append(pool.acquire(timeout=5)), daemon=True)
    worker.start()
    assert wait_until(lambda: pool.waiters == 1), "worker should be blocked waiting"
    pool.release(held)
    worker.join(timeout=1)
    assert not worker.is_alive(), "release must notify the Condition so the waiter wakes up"
    assert got == [held]


def test_context_manager_releases_connection_when_body_raises():
    pool = ConnectionPool(FakeConn, 1)
    with pytest.raises(ValueError):
        with pool.connection():
            raise ValueError("query failed")
    assert pool.stats()["in_use"] == 0, "an exception inside the block must not leak the connection"
    with pool.connection(timeout=0.05):
        pass


def test_broken_connection_is_discarded_and_capacity_returns():
    pool = ConnectionPool(FakeConn, 1)
    with pytest.raises(ConnectionError):
        with pool.connection() as conn:
            raise ConnectionError("server closed the connection")
    assert conn.closed is True
    assert pool.stats() == {"idle": 0, "in_use": 0, "created": 0}
    with pool.connection(timeout=0.05) as fresh:
        assert fresh is not conn, "a new connection can be created in the freed slot"


def test_double_release_does_not_hand_one_connection_to_two_callers():
    pool = ConnectionPool(FakeConn, 2)
    conn = pool.acquire()
    pool.release(conn)
    pool.release(conn)
    first = pool.acquire()
    second = pool.acquire()
    assert first is not second, "the same connection was lent out twice"


def test_failed_factory_frees_its_reserved_slot():
    calls = {"n": 0}

    def flaky():
        calls["n"] += 1
        if calls["n"] == 1:
            raise OSError("connect refused")
        return FakeConn()

    pool = ConnectionPool(flaky, 1)
    with pytest.raises(OSError):
        pool.acquire()
    assert pool.acquire(timeout=0.05) is not None
