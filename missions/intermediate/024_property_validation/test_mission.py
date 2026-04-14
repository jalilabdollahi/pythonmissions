import pytest
import sys
sys.path.insert(0, ".")
from broken import Server

def test_valid_port():
    s = Server("localhost", 8080)
    assert s.port == 8080

def test_port_zero_invalid():
    with pytest.raises(ValueError):
        Server("localhost", 0)

def test_address():
    s = Server("api.example.com", 443)
    assert s.address() == "api.example.com:443"
