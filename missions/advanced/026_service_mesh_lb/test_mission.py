import pytest, sys
sys.path.insert(0, ".")
from broken import WeightedLoadBalancer

def test_basic_select():
    lb = WeightedLoadBalancer()
    lb.register("h1", 80)
    ep = lb.select()
    assert ep["host"] == "h1"

def test_excludes_unhealthy():
    lb = WeightedLoadBalancer()
    lb.register("h1", 80)
    lb.register("h2", 80)
    lb.mark_health("h1", 80, False)
    for _ in range(20):
        ep = lb.select()
        assert ep["host"] == "h2"

def test_no_healthy_raises():
    lb = WeightedLoadBalancer()
    lb.register("h1", 80)
    lb.mark_health("h1", 80, False)
    with pytest.raises(RuntimeError):
        lb.select()
