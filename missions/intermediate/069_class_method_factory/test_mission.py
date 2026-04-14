import pytest, sys
sys.path.insert(0, ".")
from broken import ServiceConfig

def test_from_dict():
    cfg = ServiceConfig.from_dict({"name": "api", "host": "10.0.0.1", "port": 443})
    assert cfg.name == "api"
    assert cfg.env == "prod"
    assert isinstance(cfg, ServiceConfig)

def test_development():
    cfg = ServiceConfig.development("worker")
    assert cfg.host == "localhost"
    assert cfg.env == "dev"
    assert not cfg.is_prod()
