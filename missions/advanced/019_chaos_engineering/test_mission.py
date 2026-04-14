import pytest, sys, time
sys.path.insert(0, ".")
from broken import ChaosFramework

SERVICES = [f"svc-{i}" for i in range(10)]

def test_blast_radius_fraction():
    cf = ChaosFramework(SERVICES)
    targets = cf.blast_radius(0.3)
    assert len(targets) == 3

def test_failure_makes_unhealthy():
    cf = ChaosFramework(["api"])
    cf.inject_failure("api", duration_s=60)
    assert cf.is_healthy("api") is False

def test_latency_also_unhealthy():
    cf = ChaosFramework(["api"])
    cf.inject_latency("api", 500, duration_s=60)
    assert cf.is_healthy("api") is False

def test_expired_failure_healthy():
    cf = ChaosFramework(["api"])
    cf.inject_failure("api", duration_s=0.01)
    time.sleep(0.05)
    assert cf.is_healthy("api") is True
