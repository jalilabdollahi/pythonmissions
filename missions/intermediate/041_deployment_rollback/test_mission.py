import pytest
import sys
sys.path.insert(0, ".")
from broken import DeploymentStack

def test_deploy_and_rollback():
    d = DeploymentStack()
    d.deploy("v1.0")
    d.deploy("v2.0")
    d.rollback()
    assert d.current() == "v1.0"

def test_can_rollback():
    d = DeploymentStack()
    assert not d.can_rollback()
    d.deploy("v1.0")
    assert not d.can_rollback()
    d.deploy("v2.0")
    assert d.can_rollback()

def test_rollback_nothing():
    d = DeploymentStack()
    d.deploy("v1.0")
    with pytest.raises(RuntimeError):
        d.rollback()
