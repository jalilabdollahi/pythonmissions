import pytest, sys
sys.path.insert(0, ".")
from broken import aggregate_health, is_healthy, has_degraded

COMPS = {
    "db": {"status": "healthy"},
    "cache": {"status": "degraded"},
    "api": {"status": "healthy"},
}

def test_worst_status():
    result = aggregate_health(COMPS)
    assert result["status"] == "degraded"

def test_all_healthy():
    result = aggregate_health({"a": {"status": "healthy"}, "b": {"status": "healthy"}})
    assert is_healthy(result)

def test_has_degraded():
    result = aggregate_health(COMPS)
    assert has_degraded(result)
