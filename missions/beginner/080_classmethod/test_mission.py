import os, sys
sys.path.insert(0, os.path.dirname(__file__))

def test_creates_instance():
    from broken import Service
    svc = Service.from_dict({"name": "web", "host": "localhost", "port": 8080})
    assert isinstance(svc, Service)

def test_fields_set():
    from broken import Service
    svc = Service.from_dict({"name": "api", "host": "api.internal", "port": 443})
    assert svc.name == "api"
    assert svc.port == 443
