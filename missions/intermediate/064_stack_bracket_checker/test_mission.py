import pytest, sys
sys.path.insert(0, ".")
from broken import check_brackets, count_unmatched

def test_valid():
    assert check_brackets("{}[]()") is True
    assert check_brackets("{[()]}") is True

def test_unmatched_open():
    assert check_brackets("{[") is False

def test_wrong_close():
    assert check_brackets("{]") is False

def test_count_unmatched():
    assert count_unmatched("((") == 2
    assert count_unmatched(")(") == 2
