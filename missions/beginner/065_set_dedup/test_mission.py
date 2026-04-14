import os, sys
sys.path.insert(0, os.path.dirname(__file__))

def test_removes_duplicates():
    from broken import unique_sorted
    result = unique_sorted(["CRITICAL","WARN","CRITICAL","INFO","WARN"])
    assert len(result) == 3

def test_sorted():
    from broken import unique_sorted
    result = unique_sorted(["WARN","CRITICAL","INFO"])
    assert result == sorted(result)

def test_no_duplicates_in_result():
    from broken import unique_sorted
    result = unique_sorted(["a","b","a"])
    assert result.count("a") == 1
