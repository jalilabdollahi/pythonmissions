import os, sys
sys.path.insert(0, os.path.dirname(__file__))

def test_returns_list():
    from broken import clean_block
    result = clean_block("  host=localhost  \n  port=5432  \n")
    assert isinstance(result, list)

def test_strips_each_line():
    from broken import clean_block
    result = clean_block("  host=localhost  \n  port=5432  \n")
    assert result == ["host=localhost", "port=5432"]

def test_skips_empty_lines():
    from broken import clean_block
    result = clean_block("  host=localhost  \n\n  port=5432  \n")
    assert "" not in result
