import os, sys
sys.path.insert(0, os.path.dirname(__file__))

CFG = {"database": {"host": "db.internal", "port": 5432}}

def test_existing_nested():
    from broken import safe_get
    assert safe_get(CFG, "database", "host") == "db.internal"

def test_missing_leaf():
    from broken import safe_get
    assert safe_get(CFG, "database", "password") is None

def test_missing_top():
    from broken import safe_get
    assert safe_get(CFG, "redis", "host") is None

def test_single_key():
    from broken import safe_get
    assert safe_get({"key": "val"}, "key") == "val"
