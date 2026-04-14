import os, sys
sys.path.insert(0, os.path.dirname(__file__))

def test_strips_lines():
    from broken import process_lines
    result = process_lines(["  ERROR  ", "  WARN  "])
    assert result == ["ERROR", "WARN"]

def test_skips_empty():
    from broken import process_lines
    result = process_lines(["  ERROR  ", "", "   "])
    assert "" not in result
    assert len(result) == 1
