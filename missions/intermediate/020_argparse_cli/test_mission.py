import pytest
import sys
sys.path.insert(0, ".")
from broken import parse_deploy_args

def test_basic_parse():
    args = parse_deploy_args(["prod"])
    assert args.env == "prod"
    assert args.port == 8080

def test_port_type():
    args = parse_deploy_args(["dev", "--port", "9090"])
    assert args.port == 9090
    assert isinstance(args.port, int)
