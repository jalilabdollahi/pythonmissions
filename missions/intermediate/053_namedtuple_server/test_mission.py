import pytest, sys
sys.path.insert(0, ".")
from broken import make_server, server_url, is_production

def test_make_server():
    s = make_server("web-01", "10.0.0.1", 80)
    assert s.hostname == "web-01"
    assert s.env == "prod"

def test_server_url():
    s = make_server("api.example.com", "10.0.0.2", 443)
    assert s.hostname in server_url(s)
    assert "443" in server_url(s)

def test_is_production():
    s = make_server("prod-01", "10.0.0.3", 80, "prod")
    assert is_production(s)
    s2 = make_server("dev-01", "10.0.0.4", 80, "dev")
    assert not is_production(s2)
