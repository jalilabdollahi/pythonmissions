import pytest, sys
sys.path.insert(0, ".")
from broken import merge_sort

def test_sort_basic():
    assert merge_sort([3, 1, 4, 1, 5, 9]) == [1, 1, 3, 4, 5, 9]

def test_empty():
    assert merge_sort([]) == []

def test_single():
    assert merge_sort([42]) == [42]

def test_timestamps():
    ts = [1700000050, 1700000010, 1700000030]
    assert merge_sort(ts) == [1700000010, 1700000030, 1700000050]
