import pytest, sys
sys.path.insert(0, ".")
from broken import TenantManager

def test_store_and_retrieve():
    tm = TenantManager()
    tm.create_tenant("t1")
    tm.store("t1", "config", {"env": "prod"})
    assert tm.retrieve("t1", "config")["env"] == "prod"

def test_quota_before_store():
    tm = TenantManager()
    tm.create_tenant("t1", quota=5)
    with pytest.raises(RuntimeError):
        tm.store("t1", "bigdata", "x" * 100, size=10)
    assert "bigdata" not in (tm._tenants["t1"]["data"])  # not stored

def test_tenant_isolation():
    tm = TenantManager()
    tm.create_tenant("t1"); tm.create_tenant("t2")
    tm.store("t1", "secret", "t1-value")
    tm.store("t2", "secret", "t2-value")
    keys_t1 = tm.list_keys("t1")
    assert "secret" in keys_t1
    assert len(keys_t1) == 1  # only t1's key
