import pytest, sys, time
sys.path.insert(0, ".")
from broken import ServiceRegistry

def test_register_and_lookup():
    r = ServiceRegistry()
    r.register("api", "10.0.0.1", 8080, ttl=60)
    instances = r.lookup("api")
    assert ("10.0.0.1", 8080) in instances

def test_expired_not_returned():
    r = ServiceRegistry()
    r.register("api", "10.0.0.1", 8080, ttl=0.01)
    time.sleep(0.05)
    instances = r.lookup("api")
    assert instances == []

def test_no_duplicate_on_re_register():
    r = ServiceRegistry()
    r.register("api", "10.0.0.1", 8080)
    r.register("api", "10.0.0.1", 8080)
    instances = r.lookup("api")
    assert instances.count(("10.0.0.1", 8080)) == 1
