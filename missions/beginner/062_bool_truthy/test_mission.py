import os, sys
sys.path.insert(0, os.path.dirname(__file__))

def test_true_string():
    from broken import is_enabled
    assert is_enabled("true") is True

def test_false_string():
    from broken import is_enabled
    assert is_enabled("false") is False

def test_case_insensitive():
    from broken import is_enabled
    assert is_enabled("True") is True
    assert is_enabled("FALSE") is False
