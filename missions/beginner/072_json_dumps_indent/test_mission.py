import os, sys, json
sys.path.insert(0, os.path.dirname(__file__))

def test_is_valid_json():
    from broken import pretty_json
    result = pretty_json({"key": "val"})
    assert json.loads(result) == {"key": "val"}

def test_has_newlines():
    from broken import pretty_json
    result = pretty_json({"a": 1, "b": 2})
    assert "\n" in result

def test_indented():
    from broken import pretty_json
    result = pretty_json({"a": 1})
    assert "  " in result
