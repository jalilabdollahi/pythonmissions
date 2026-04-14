import os, sys
sys.path.insert(0, os.path.dirname(__file__))

def test_iterable():
    from broken import ServerPool
    pool = ServerPool(["web-01", "web-02", "web-03"])
    result = list(pool)
    assert result == ["web-01", "web-02", "web-03"]

def test_for_loop():
    from broken import ServerPool
    pool = ServerPool(["web-01", "web-02"])
    collected = []
    for h in pool:
        collected.append(h)
    assert collected == ["web-01", "web-02"]
