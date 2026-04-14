import os, sys
sys.path.insert(0, os.path.dirname(__file__))

def test_returns_dict():
    from broken import build_port_map
    result = build_port_map(["web", "api"], [80, 8080])
    assert isinstance(result, dict)

def test_correct_mapping():
    from broken import build_port_map
    result = build_port_map(["web", "api", "db"], [80, 8080, 5432])
    assert result["web"] == 80
    assert result["api"] == 8080
    assert result["db"] == 5432
