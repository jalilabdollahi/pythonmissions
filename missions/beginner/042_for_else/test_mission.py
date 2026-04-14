import os, sys
sys.path.insert(0, os.path.dirname(__file__))

REGISTRY = [{"name": "web", "port": 80}, {"name": "api", "port": 8080}]

def test_found_prints_svc(capsys):
    from broken import find_service
    find_service(REGISTRY, "web")
    out = capsys.readouterr().out
    assert "Found" in out
    assert "not found" not in out

def test_not_found_prints_message(capsys):
    from broken import find_service
    find_service(REGISTRY, "db")
    out = capsys.readouterr().out
    assert "not found" in out
