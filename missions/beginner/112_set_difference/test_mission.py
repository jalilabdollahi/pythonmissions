import os, sys
sys.path.insert(0, os.path.dirname(__file__))

def test_new_only():
    from broken import new_alerts
    prev = {"disk-full", "high-cpu"}
    curr = {"disk-full", "oom", "network-down"}
    result = new_alerts(prev, curr)
    assert result == {"oom", "network-down"}

def test_nothing_new():
    from broken import new_alerts
    assert new_alerts({"a"}, {"a"}) == set()

def test_resolved_not_included():
    from broken import new_alerts
    result = new_alerts({"disk-full", "high-cpu"}, {"disk-full"})
    assert "high-cpu" not in result
