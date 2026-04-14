import os, sys
sys.path.insert(0, os.path.dirname(__file__))

def test_removes_existing():
    from broken import remove_if_present
    pool = ["web-01", "web-02", "web-03"]
    remove_if_present(pool, "web-02")
    assert pool == ["web-01", "web-03"]

def test_no_crash_on_missing():
    from broken import remove_if_present
    pool = ["web-01"]
    remove_if_present(pool, "web-99")  # should not raise
    assert pool == ["web-01"]

def test_empty_pool():
    from broken import remove_if_present
    pool = []
    remove_if_present(pool, "web-01")
    assert pool == []
