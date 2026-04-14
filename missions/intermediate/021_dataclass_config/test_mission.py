import pytest
import sys
sys.path.insert(0, ".")
from broken import ServiceConfig

def test_create_config():
    cfg = ServiceConfig(port=8080)
    assert cfg.host == "localhost"
    assert cfg.port == 8080
    assert cfg.debug is False

def test_invalid_port():
    with pytest.raises(ValueError):
        ServiceConfig(port=99999)

def test_custom_host():
    cfg = ServiceConfig(port=443, host="example.com")
    assert cfg.host == "example.com"
