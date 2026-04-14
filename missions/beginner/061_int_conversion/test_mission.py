import os, sys
sys.path.insert(0, os.path.dirname(__file__))

def test_returns_int():
    from broken import get_port
    assert isinstance(get_port("8080"), int)

def test_correct_value():
    from broken import get_port
    assert get_port("8080") == 8080

def test_port_443():
    from broken import get_port
    assert get_port("443") == 443
