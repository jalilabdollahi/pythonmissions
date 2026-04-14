import pytest, sys, json
sys.path.insert(0, ".")
from broken import MockServer

def test_get_route():
    server = MockServer()
    server.register("GET", "/health", {"status": "ok"})
    status, body = server.handle("GET", "/health")
    assert status == 200
    data = json.loads(body)
    assert data["status"] == "ok"

def test_method_specific():
    server = MockServer()
    server.register("GET", "/resource", {"id": 1})
    server.register("POST", "/resource", {"created": True}, status=201)
    status, _ = server.handle("POST", "/resource")
    assert status == 201

def test_not_found():
    server = MockServer()
    status, _ = server.handle("GET", "/nonexistent")
    assert status == 404
