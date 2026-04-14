import os, sys
sys.path.insert(0, os.path.dirname(__file__))

def test_returns_list():
    from broken import int_ports
    assert isinstance(int_ports(["80", "443"]), list)

def test_correct_values():
    from broken import int_ports
    assert int_ports(["80", "443", "8080"]) == [80, 443, 8080]
