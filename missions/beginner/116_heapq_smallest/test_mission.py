import os, sys
sys.path.insert(0, os.path.dirname(__file__))

def test_returns_largest():
    from broken import slowest_three
    times = [120, 340, 89, 2000, 456, 1500, 78, 900]
    result = slowest_three(times)
    assert 2000 in result and 1500 in result and 900 in result

def test_count():
    from broken import slowest_three
    assert len(slowest_three([1,2,3,4,5])) == 3
