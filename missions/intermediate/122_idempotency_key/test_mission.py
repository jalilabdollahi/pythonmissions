import pytest, sys, time
sys.path.insert(0, ".")
from broken import IdempotencyManager

def test_case_insensitive():
    mgr = IdempotencyManager()
    mgr.set("KEY-ABC", {"charged": True})
    assert mgr.get("key-abc") is not None
    assert mgr.get("KEY-ABC") is not None

def test_is_duplicate():
    mgr = IdempotencyManager()
    mgr.set("pay-001", {"amount": 100})
    assert mgr.is_duplicate("pay-001") is True
    assert mgr.is_duplicate("pay-002") is False

def test_expired():
    mgr = IdempotencyManager(ttl=0.01)
    mgr.set("tx-001", {"ok": True})
    time.sleep(0.05)
    assert mgr.get("tx-001") is None
