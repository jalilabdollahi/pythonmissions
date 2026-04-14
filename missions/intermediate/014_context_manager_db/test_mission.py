import pytest
import sys
sys.path.insert(0, ".")
from broken import FakeDB, query_db

def test_context_manager():
    db = FakeDB("postgres://localhost/test")
    with db as conn:
        assert conn.connected
    assert not db.connected

def test_query_db():
    result = query_db("postgres://localhost/test", "SELECT 1")
    assert "SELECT 1" in result
