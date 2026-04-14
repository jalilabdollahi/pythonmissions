import os, sys
sys.path.insert(0, os.path.dirname(__file__))

def test_returns_from_list():
    from broken import pick_server
    pool = ["web-01", "web-02", "web-03"]
    for _ in range(20):
        assert pick_server(pool) in pool

def test_single_server():
    from broken import pick_server
    assert pick_server(["web-01"]) == "web-01"
