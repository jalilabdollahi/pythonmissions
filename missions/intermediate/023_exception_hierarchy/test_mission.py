import pytest
import sys
sys.path.insert(0, ".")
from broken import DeploymentError, TimeoutError, deploy, safe_deploy

def test_exception_is_exception():
    assert issubclass(DeploymentError, Exception)

def test_timeout_is_deployment():
    assert issubclass(TimeoutError, DeploymentError)

def test_deploy_success():
    assert "myapp" in deploy("myapp")

def test_safe_deploy_timeout():
    result = safe_deploy("myapp", timeout=-1)
    assert result == "timed out"

def test_safe_deploy_no_service():
    result = safe_deploy("")
    assert result == "deployment failed"
