import pytest, sys, time
sys.path.insert(0, ".")
from broken import AlertDeduplicator

ALERT = {"name": "DiskFull", "labels": {"host": "web-01", "severity": "critical"}}

def test_first_not_duplicate():
    d = AlertDeduplicator()
    assert d.is_duplicate(ALERT) is False

def test_second_is_duplicate():
    d = AlertDeduplicator()
    d.is_duplicate(ALERT)
    assert d.is_duplicate(ALERT) is True

def test_expired_not_duplicate():
    d = AlertDeduplicator(ttl=0.05)
    d.is_duplicate(ALERT)
    time.sleep(0.1)
    assert d.is_duplicate(ALERT) is False
