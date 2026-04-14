import pytest
import sys
sys.path.insert(0, ".")
from broken import setup_metrics, record_request, update_connections

def test_setup():
    req, conns = setup_metrics()
    assert req is not None
    assert conns is not None

def test_record_request():
    record_request("GET", "/api/health")

def test_update_connections():
    update_connections(42)
    _, conns = setup_metrics()
    assert conns.val == 42
