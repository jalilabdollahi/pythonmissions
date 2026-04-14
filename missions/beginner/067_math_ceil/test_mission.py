import os, sys
sys.path.insert(0, os.path.dirname(__file__))

def test_rounds_up():
    from broken import replica_count
    assert replica_count(10, 3) == 4

def test_exact_division():
    from broken import replica_count
    assert replica_count(9, 3) == 3

def test_single_request():
    from broken import replica_count
    assert replica_count(1, 10) == 1
