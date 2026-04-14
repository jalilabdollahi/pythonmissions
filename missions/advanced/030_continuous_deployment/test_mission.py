import pytest, sys
sys.path.insert(0, ".")
from broken import CDEngine

def test_promote_all_gates_must_pass():
    engine = CDEngine()
    engine.deploy("v1", "dev")
    engine.add_gate("dev", "staging", lambda d: True)
    engine.add_gate("dev", "staging", lambda d: False)
    with pytest.raises(RuntimeError):
        engine.promote("dev", "staging")

def test_promote_succeeds():
    engine = CDEngine()
    engine.deploy("v2", "dev")
    engine.add_gate("dev", "staging", lambda d: True)
    version = engine.promote("dev", "staging")
    assert version == "v2"
    assert engine._deployments["staging"]["version"] == "v2"

def test_auto_rollback_on_failure():
    engine = CDEngine()
    engine.deploy("v1", "prod")
    engine.deploy("v2", "prod")
    rolled_back = engine.auto_rollback("prod", lambda d: False)
    assert rolled_back is True
    assert engine._deployments["prod"]["version"] == "v1"

def test_no_rollback_when_healthy():
    engine = CDEngine()
    engine.deploy("v1", "prod")
    engine.deploy("v2", "prod")
    rolled_back = engine.auto_rollback("prod", lambda d: True)
    assert rolled_back is False
