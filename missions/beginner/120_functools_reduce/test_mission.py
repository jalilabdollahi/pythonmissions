import os, sys
sys.path.insert(0, os.path.dirname(__file__))

def test_product():
    from broken import total_capacity
    assert total_capacity([2, 3, 4]) == 24

def test_single():
    from broken import total_capacity
    assert total_capacity([5]) == 5

def test_empty():
    from broken import total_capacity
    assert total_capacity([]) == 1
