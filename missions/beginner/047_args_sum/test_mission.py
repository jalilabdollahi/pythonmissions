import os, sys
sys.path.insert(0, os.path.dirname(__file__))

def test_three_args():
    from broken import total
    assert total(10, 20, 30) == 60

def test_one_arg():
    from broken import total
    assert total(5) == 5

def test_no_args():
    from broken import total
    assert total() == 0
