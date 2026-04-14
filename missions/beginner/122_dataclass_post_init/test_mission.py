import os, sys, pytest
sys.path.insert(0, os.path.dirname(__file__))

def test_valid_service():
    from broken import Service
    s = Service("web", 8080)
    assert s.port == 8080

def test_invalid_port_raises():
    from broken import Service
    with pytest.raises(ValueError):
        Service("web", 99999)

def test_zero_port_raises():
    from broken import Service
    with pytest.raises(ValueError):
        Service("web", 0)
