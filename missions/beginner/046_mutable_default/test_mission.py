import os, sys
sys.path.insert(0, os.path.dirname(__file__))

def test_default_is_empty():
    from broken import new_deployment
    d = new_deployment("prod")
    assert d["servers"] == []

def test_independent_defaults():
    from broken import new_deployment
    d1 = new_deployment("prod")
    d1["servers"].append("web-01")
    d2 = new_deployment("staging")
    assert d2["servers"] == []

def test_custom_servers():
    from broken import new_deployment
    d = new_deployment("prod", ["web-01"])
    assert d["servers"] == ["web-01"]
