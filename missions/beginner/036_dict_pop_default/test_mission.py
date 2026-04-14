import os, sys
sys.path.insert(0, os.path.dirname(__file__))

def test_removes_existing():
    from broken import remove_flag
    flags = {"dark_mode": True}
    val = remove_flag(flags, "dark_mode")
    assert val is True
    assert "dark_mode" not in flags

def test_missing_returns_false():
    from broken import remove_flag
    flags = {}
    assert remove_flag(flags, "nonexistent") is False

def test_empty_dict():
    from broken import remove_flag
    assert remove_flag({}, "any") is False
