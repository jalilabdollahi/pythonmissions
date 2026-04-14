import pytest, sys
sys.path.insert(0, ".")
from broken import DeployRequest

def test_valid_request():
    r = DeployRequest(service="api", version="v1.2.3")
    assert r.service == "api"
    assert r.env == "prod"
    assert r.replicas == 1

def test_defaults():
    r = DeployRequest(service="worker", version="v2.0")
    assert r.tags == []
    assert r.replicas == 1
