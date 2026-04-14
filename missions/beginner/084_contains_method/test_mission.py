import os, sys
sys.path.insert(0, os.path.dirname(__file__))

def test_contains_existing():
    from broken import ServerPool
    pool = ServerPool(["web-01", "web-02"])
    assert "web-01" in pool

def test_not_contains():
    from broken import ServerPool
    pool = ServerPool(["web-01", "web-02"])
    assert "web-99" not in pool

def test_after_add():
    from broken import ServerPool
    pool = ServerPool([])
    pool.add("web-01")
    assert "web-01" in pool
