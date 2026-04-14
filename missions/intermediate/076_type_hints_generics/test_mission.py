import pytest, sys
sys.path.insert(0, ".")
from broken import TypedCache

def test_set_get():
    c: TypedCache[str, int] = TypedCache()
    c.set("ttl", 3600)
    assert c.get("ttl") == 3600

def test_missing():
    c: TypedCache[str, str] = TypedCache()
    assert c.get("missing") is None

def test_keys():
    c: TypedCache[str, bool] = TypedCache()
    c.set("debug", True)
    assert "debug" in c.keys()
