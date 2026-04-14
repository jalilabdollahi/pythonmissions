import pytest, sys
sys.path.insert(0, ".")
from broken import ConnectionPool

def test_execute():
    pool = ConnectionPool(3)
    result = pool.execute("SELECT 1")
    assert "SELECT 1" in result

def test_pool_returns_connection():
    pool = ConnectionPool(1)
    pool.execute("SELECT 1")
    # Should be able to execute again (connection was returned)
    result = pool.execute("SELECT 2")
    assert "SELECT 2" in result

def test_exhausted_raises():
    pool = ConnectionPool(1)
    conn = pool.acquire()
    with pytest.raises(RuntimeError):
        pool.acquire()
    pool.release(conn)
