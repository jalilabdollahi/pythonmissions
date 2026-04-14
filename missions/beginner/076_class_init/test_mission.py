import os, sys
sys.path.insert(0, os.path.dirname(__file__))

def test_creates_instance():
    from broken import Service
    svc = Service("web", "localhost", 8080)
    assert svc.name == "web"

def test_endpoint():
    from broken import Service
    svc = Service("web", "localhost", 8080)
    assert svc.endpoint() == "localhost:8080"

def test_stores_port():
    from broken import Service
    svc = Service("api", "api.internal", 443)
    assert svc.port == 443
