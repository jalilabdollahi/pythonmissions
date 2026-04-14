import os, sys
sys.path.insert(0, os.path.dirname(__file__))

def test_simple():
    from broken import split_host_port
    assert split_host_port("localhost:8080") == ("localhost", "8080")

def test_ip():
    from broken import split_host_port
    host, port = split_host_port("10.0.0.1:443")
    assert host == "10.0.0.1"
    assert port == "443"
