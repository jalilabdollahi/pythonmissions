import os, sys
sys.path.insert(0, os.path.dirname(__file__))

def test_iterates_correctly():
    from broken import IPRange
    result = list(IPRange(1, 3))
    assert result == [1, 2, 3]

def test_correct_count():
    from broken import IPRange
    assert len(list(IPRange(10, 5))) == 5

def test_empty():
    from broken import IPRange
    assert list(IPRange(1, 0)) == []
