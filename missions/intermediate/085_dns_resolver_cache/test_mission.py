import pytest, sys, time
sys.path.insert(0, ".")
from broken import DNSCache

def test_set_get():
    c = DNSCache()
    c.set("api.example.com", "10.0.0.1", ttl=60)
    assert c.get("api.example.com") == "10.0.0.1"

def test_expired():
    c = DNSCache()
    c.set("api.example.com", "10.0.0.1", ttl=0.01)
    time.sleep(0.05)
    assert c.get("api.example.com") is None

def test_cleanup():
    c = DNSCache()
    c.set("old.example.com", "1.2.3.4", ttl=0.01)
    c.set("new.example.com", "5.6.7.8", ttl=60)
    time.sleep(0.05)
    c.cleanup()
    assert "old.example.com" not in c._cache
    assert "new.example.com" in c._cache
