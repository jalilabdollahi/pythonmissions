import pytest, sys
sys.path.insert(0, ".")
from broken import binary_search, find_log_entry, count_in_range

def test_found():
    assert binary_search([1,3,5,7,9], 5) == 2

def test_not_found():
    assert binary_search([1,2,3], 4) == -1

def test_find_log():
    logs = [(1, "boot"), (5, "ready"), (9, "error")]
    assert find_log_entry(logs, 5) == "ready"

def test_count_in_range():
    arr = [1, 2, 3, 4, 5]
    assert count_in_range(arr, 2, 4) == 3
