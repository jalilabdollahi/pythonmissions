import os, sys
sys.path.insert(0, os.path.dirname(__file__))

def test_returns_string():
    from broken import make_separator
    assert isinstance(make_separator(40), str)

def test_correct_length():
    from broken import make_separator
    assert len(make_separator(40)) == 40

def test_all_dashes():
    from broken import make_separator
    assert make_separator(5) == "-----"

def test_zero():
    from broken import make_separator
    assert make_separator(0) == ""
