import os, sys
sys.path.insert(0, os.path.dirname(__file__))

def test_default_when_missing(monkeypatch):
    monkeypatch.delenv("DB_PASSWORD", raising=False)
    from broken import get_db_password
    assert get_db_password() == "changeme"

def test_returns_value(monkeypatch):
    monkeypatch.setenv("DB_PASSWORD", "s3cr3t")
    from broken import get_db_password
    assert get_db_password() == "s3cr3t"
