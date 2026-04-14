import os, sys
sys.path.insert(0, os.path.dirname(__file__))

def test_finds_max():
    from broken import max_cpu
    assert max_cpu([45.2, 78.9, 92.1, 55.0]) == 92.1

def test_empty_returns_zero():
    from broken import max_cpu
    assert max_cpu([]) == 0

def test_single():
    from broken import max_cpu
    assert max_cpu([42.0]) == 42.0
