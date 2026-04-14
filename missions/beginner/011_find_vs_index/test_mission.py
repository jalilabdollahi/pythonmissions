import os, sys
sys.path.insert(0, os.path.dirname(__file__))

def test_finds_port():
    from broken import find_port_offset
    assert find_port_offset("service port=8080") == 8

def test_returns_negative_when_missing():
    from broken import find_port_offset
    assert find_port_offset("service name=web") == -1

def test_at_start():
    from broken import find_port_offset
    assert find_port_offset("port=80") == 0
