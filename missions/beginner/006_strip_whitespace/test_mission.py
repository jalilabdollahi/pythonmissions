import os, sys
sys.path.insert(0, os.path.dirname(__file__))

def test_removes_trailing_space():
    from broken import clean_name
    assert clean_name("prod-web-01   ") == "prod-web-01"

def test_removes_leading_space():
    from broken import clean_name
    assert clean_name("   prod-web-01") == "prod-web-01"

def test_removes_both_sides():
    from broken import clean_name
    assert clean_name("  prod-web-01  ") == "prod-web-01"

def test_removes_newline():
    from broken import clean_name
    assert clean_name("prod-web-01\n") == "prod-web-01"

def test_batch_clean():
    from broken import batch_clean
    result = batch_clean(["  web-01  ", "  db-01\n"])
    assert result == ["web-01", "db-01"]
