import os, sys
sys.path.insert(0, os.path.dirname(__file__))

def test_returns_port():
    from broken import get_port, Server
    s = Server("web-01", "localhost", 8080)
    assert get_port(s) == 8080

def test_not_name():
    from broken import get_port, Server
    s = Server("web-01", "localhost", 443)
    assert get_port(s) == 443
