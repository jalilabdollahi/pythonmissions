import pytest, sys
sys.path.insert(0, ".")
from broken import config_diff, format_diff

OLD = {"host": "localhost", "port": 8080, "debug": True}
NEW = {"host": "prod.example.com", "port": 8080, "workers": 4}

def test_added():
    d = config_diff(OLD, NEW)
    assert "workers" in d["added"]

def test_removed():
    d = config_diff(OLD, NEW)
    assert "debug" in d["removed"]

def test_changed():
    d = config_diff(OLD, NEW)
    assert "host" in d["changed"]
    assert d["changed"]["host"]["old"] == "localhost"

def test_unchanged():
    d = config_diff(OLD, NEW)
    assert "port" not in d["changed"]
