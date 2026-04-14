import pytest, sys
sys.path.insert(0, ".")
from broken import diff_envs, has_drift, critical_drift

A = {"HOST": "prod.example.com", "PORT": "8080", "DEBUG": "false"}
B = {"HOST": "staging.example.com", "PORT": "8080", "WORKERS": "4"}

def test_diff_envs():
    diffs = diff_envs(A, B)
    assert "HOST" in diffs
    assert "PORT" not in diffs
    assert "WORKERS" in diffs

def test_has_drift():
    assert has_drift(A, B)
    assert not has_drift(A, A)

def test_critical_drift():
    result = critical_drift(A, B, ["HOST", "PORT"])
    assert "HOST" in result
    assert "PORT" not in result
