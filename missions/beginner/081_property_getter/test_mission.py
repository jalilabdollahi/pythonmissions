import os, sys
sys.path.insert(0, os.path.dirname(__file__))

def test_endpoint_is_string():
    from broken import Service
    svc = Service("localhost", 8080)
    assert isinstance(svc.endpoint, str)

def test_endpoint_value():
    from broken import Service
    svc = Service("localhost", 8080)
    assert svc.endpoint == "localhost:8080"

def test_no_call_needed():
    from broken import Service
    svc = Service("api.internal", 443)
    assert svc.endpoint == "api.internal:443"
