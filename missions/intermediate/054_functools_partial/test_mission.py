import pytest, sys
sys.path.insert(0, ".")
from broken import make_deployer, dry_deploy, deploy

def test_make_deployer():
    prod_deploy = make_deployer("prod")
    result = prod_deploy("api-service")
    assert result["env"] == "prod"
    assert result["service"] == "api-service"

def test_dry_deploy():
    result = dry_deploy("worker", "staging")
    assert result["dry_run"] is True
