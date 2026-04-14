import pytest, sys
sys.path.insert(0, ".")
from broken import MigrationManager

def test_dual_write():
    db = {}
    m = MigrationManager(db)
    m.advance_phase()  # -> dual_write
    m.write_user("u1", "Alice@Example.com", "alice@example.com")
    assert db["u1"].get("email") == "Alice@Example.com"
    assert db["u1"].get("email_v2") == "alice@example.com"

def test_backfill_advances_phase():
    db = {"u1": {"email": "Bob@Example.com"}}
    m = MigrationManager(db)
    m.advance_phase()  # -> dual_write
    m.backfill()       # should advance to new_only
    assert m.phase == m.PHASE_NEW
    assert db["u1"]["email_v2"] == "bob@example.com"
