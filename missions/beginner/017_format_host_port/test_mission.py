import os, sys
sys.path.insert(0, os.path.dirname(__file__))

def test_basic():
    from broken import format_endpoint
    assert format_endpoint("web-01", 8080) == "web-01:8080"

def test_port_443():
    from broken import format_endpoint
    assert format_endpoint("api.internal", 443) == "api.internal:443"

def test_localhost():
    from broken import format_endpoint
    assert format_endpoint("localhost", 3000) == "localhost:3000"
