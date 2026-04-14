import pytest, sys
sys.path.insert(0, ".")
from broken import DeployServiceClient, DeployResponse
from unittest.mock import MagicMock

def test_deploy():
    stub = MagicMock()
    stub.Deploy.return_value = DeployResponse("dep-001", "RUNNING")
    client = DeployServiceClient(stub)
    dep_id = client.deploy("api", "v2.0")
    assert dep_id == "dep-001"
    call_arg = stub.Deploy.call_args[0][0]
    assert hasattr(call_arg, "service")

def test_get_status():
    stub = MagicMock()
    stub.GetStatus.return_value = DeployResponse("dep-001", "SUCCEEDED")
    client = DeployServiceClient(stub)
    status = client.get_status("dep-001")
    assert status == "SUCCEEDED"
