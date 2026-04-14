import os, sys
sys.path.insert(0, os.path.dirname(__file__))

def test_staging():
    from broken import normalize_env
    assert normalize_env("staging") == "STAGING"

def test_production():
    from broken import normalize_env
    assert normalize_env("production") == "PRODUCTION"

def test_already_upper():
    from broken import normalize_env
    assert normalize_env("PROD") == "PROD"

def test_mixed_case():
    from broken import normalize_env
    assert normalize_env("Dev") == "DEV"
