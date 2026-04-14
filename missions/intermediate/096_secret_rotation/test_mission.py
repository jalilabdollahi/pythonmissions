import pytest, sys
sys.path.insert(0, ".")
from broken import SecretRotationManager
from datetime import datetime, timedelta

def test_create_and_get():
    mgr = SecretRotationManager()
    mgr.create("db_password")
    val = mgr.get("db_password")
    assert val is not None
    assert len(val) == 64  # token_hex(32) = 64 hex chars

def test_needs_rotation_new():
    mgr = SecretRotationManager(rotation_days=90)
    mgr.create("api_key")
    assert not mgr.needs_rotation("api_key")

def test_needs_rotation_old():
    mgr = SecretRotationManager(rotation_days=90)
    mgr.create("api_key")
    mgr._secrets["api_key"]["created_at"] = datetime.utcnow() - timedelta(days=100)
    assert mgr.needs_rotation("api_key")

def test_age_days():
    mgr = SecretRotationManager()
    mgr.create("token")
    mgr._secrets["token"]["created_at"] = datetime.utcnow() - timedelta(days=5)
    assert mgr.secret_age_days("token") == 5
