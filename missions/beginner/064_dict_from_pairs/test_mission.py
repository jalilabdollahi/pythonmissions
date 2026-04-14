import os, sys
sys.path.insert(0, os.path.dirname(__file__))

def test_returns_dict():
    from broken import parse_kv_lines
    result = parse_kv_lines(["host=localhost", "port=5432"])
    assert isinstance(result, dict)

def test_correct_values():
    from broken import parse_kv_lines
    result = parse_kv_lines(["host=localhost", "port=5432"])
    assert result["host"] == "localhost"
    assert result["port"] == "5432"

def test_skips_non_kv():
    from broken import parse_kv_lines
    result = parse_kv_lines(["# comment", "host=localhost"])
    assert "# comment" not in result
