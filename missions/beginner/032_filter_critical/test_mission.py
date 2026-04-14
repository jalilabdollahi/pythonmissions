import os, sys
sys.path.insert(0, os.path.dirname(__file__))

ALERTS = [
    {"msg": "disk full", "severity": "CRITICAL"},
    {"msg": "high cpu", "severity": "WARN"},
    {"msg": "OOM", "severity": "CRITICAL"},
    {"msg": "slow query", "severity": "INFO"},
]

def test_returns_only_critical():
    from broken import filter_critical
    result = filter_critical(ALERTS)
    assert all(a["severity"] == "CRITICAL" for a in result)

def test_correct_count():
    from broken import filter_critical
    assert len(filter_critical(ALERTS)) == 2

def test_empty_input():
    from broken import filter_critical
    assert filter_critical([]) == []
