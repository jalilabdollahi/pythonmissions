import os, sys
sys.path.insert(0, os.path.dirname(__file__))

def test_returns_last():
    from broken import pop_last
    q = ["deploy-db", "deploy-api", "smoke-test"]
    assert pop_last(q) == "smoke-test"

def test_removes_last():
    from broken import pop_last
    q = ["deploy-db", "deploy-api", "smoke-test"]
    pop_last(q)
    assert q == ["deploy-db", "deploy-api"]

def test_single_item():
    from broken import pop_last
    q = ["only-task"]
    assert pop_last(q) == "only-task"
    assert q == []
