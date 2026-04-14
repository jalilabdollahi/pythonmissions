import os, sys
sys.path.insert(0, os.path.dirname(__file__))

def test_returns_reversed():
    from broken import reversed_order
    assert reversed_order(["a", "b", "c"]) == ["c", "b", "a"]

def test_returns_list_not_none():
    from broken import reversed_order
    assert reversed_order(["a", "b"]) is not None

def test_original_unchanged():
    from broken import reversed_order
    steps = ["db-migrate", "backend", "frontend"]
    reversed_order(steps)
    assert steps == ["db-migrate", "backend", "frontend"]
