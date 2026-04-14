import os, sys
sys.path.insert(0, os.path.dirname(__file__))

def test_returns_correct_field():
    from broken import parse_field
    assert parse_field("prod,web-01,8080,us-east-1", 2) == "8080"

def test_first_field():
    from broken import parse_field
    assert parse_field("prod,web-01,8080,us-east-1", 0) == "prod"

def test_last_field():
    from broken import parse_field
    assert parse_field("prod,web-01,8080,us-east-1", 3) == "us-east-1"

def test_with_spaces():
    from broken import parse_field
    assert parse_field("prod, web-01, 8080", 1) == "web-01"
