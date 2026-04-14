import os, sys
sys.path.insert(0, os.path.dirname(__file__))

def test_valid_ip():
    from broken import NetworkUtil
    assert NetworkUtil.validate_ip("10.0.0.1") is True

def test_invalid_ip():
    from broken import NetworkUtil
    assert NetworkUtil.validate_ip("not-an-ip") is False

def test_no_instance_needed():
    from broken import NetworkUtil
    assert NetworkUtil.validate_ip("192.168.1.1") is True
