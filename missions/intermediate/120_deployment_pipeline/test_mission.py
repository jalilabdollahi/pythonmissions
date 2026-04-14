import pytest, sys
sys.path.insert(0, ".")
from broken import DeploymentPipeline

def test_all_success():
    p = DeploymentPipeline()
    p.add_stage("build", lambda ctx: "built")
    p.add_stage("test", lambda ctx: "passed")
    p.add_stage("deploy", lambda ctx: "deployed")
    result = p.run({})
    assert result["success"] is True
    assert len(result["stages"]) == 3

def test_stops_on_failure():
    p = DeploymentPipeline()
    p.add_stage("build", lambda ctx: "built")
    p.add_stage("test", lambda ctx: (_ for _ in ()).throw(ValueError("tests failed")))
    p.add_stage("deploy", lambda ctx: "deployed")
    result = p.run({})
    assert result["success"] is False
    assert len(result["stages"]) == 2  # stopped after test stage
