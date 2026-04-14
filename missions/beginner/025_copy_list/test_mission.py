import os, sys
sys.path.insert(0, os.path.dirname(__file__))

def test_returns_equal_content():
    from broken import copy_allowlist
    original = ["10.0.0.1", "10.0.0.2"]
    result = copy_allowlist(original)
    assert result == original

def test_is_independent():
    from broken import copy_allowlist
    original = ["10.0.0.1", "10.0.0.2"]
    result = copy_allowlist(original)
    result.append("10.0.0.99")
    assert "10.0.0.99" not in original

def test_not_same_object():
    from broken import copy_allowlist
    original = ["10.0.0.1"]
    result = copy_allowlist(original)
    assert result is not original
