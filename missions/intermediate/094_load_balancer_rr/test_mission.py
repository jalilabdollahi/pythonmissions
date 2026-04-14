import pytest, sys
sys.path.insert(0, ".")
from broken import RoundRobinLB

def test_round_robin():
    lb = RoundRobinLB(["s1", "s2", "s3"])
    results = [lb.next_server() for _ in range(6)]
    assert results == ["s1", "s2", "s3", "s1", "s2", "s3"]

def test_skips_unhealthy():
    lb = RoundRobinLB(["s1", "s2", "s3"])
    lb.mark_unhealthy("s2")
    results = {lb.next_server() for _ in range(4)}
    assert "s2" not in results

def test_no_servers():
    lb = RoundRobinLB(["s1"])
    lb.mark_unhealthy("s1")
    with pytest.raises(RuntimeError):
        lb.next_server()
