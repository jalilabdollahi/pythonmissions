import pytest, sys
sys.path.insert(0, ".")
from broken import ConfigBuilder, Validatable

class ServerConfig:
    def __init__(self, host, port):
        self.host = host
        self.port = port
    def validate(self):
        return bool(self.host) and 0 < self.port < 65536
    def to_dict(self):
        return {"host": self.host, "port": self.port}

def test_build_valid():
    builder = ConfigBuilder(ServerConfig)
    cfg = builder.set("host", "localhost").set("port", 8080).build()
    assert cfg.host == "localhost"
    assert cfg.port == 8080

def test_build_invalid():
    builder = ConfigBuilder(ServerConfig)
    with pytest.raises(ValueError):
        builder.set("host", "").set("port", 0).build()

def test_validatable_protocol():
    cfg = ServerConfig("h", 80)
    assert isinstance(cfg, Validatable)
