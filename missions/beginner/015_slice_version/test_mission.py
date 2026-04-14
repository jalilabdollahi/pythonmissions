import os, sys
sys.path.insert(0, os.path.dirname(__file__))

def test_single_digit():
    from broken import get_major
    assert get_major("2.14.3") == "2"

def test_double_digit():
    from broken import get_major
    assert get_major("10.0.1") == "10"

def test_zero():
    from broken import get_major
    assert get_major("0.9.0") == "0"
