import pytest
import sys
sys.path.insert(0, ".")
from broken import build_select

def test_no_conditions():
    q, p = build_select("users")
    assert q == "SELECT * FROM users"
    assert p == []

def test_single_condition():
    q, p = build_select("users", {"status": "active"})
    assert "WHERE status = ?" in q
    assert p == ["active"]

def test_multiple_conditions():
    q, p = build_select("servers", {"env": "prod", "status": "up"})
    assert " AND " in q
    assert len(p) == 2

def test_limit_parameterized():
    q, p = build_select("logs", limit=100)
    assert "LIMIT ?" in q
    assert 100 in p
