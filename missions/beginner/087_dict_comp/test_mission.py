import os, sys
sys.path.insert(0, os.path.dirname(__file__))

SERVERS = [{"name":"web-01","status":"healthy"},{"name":"web-02","status":"down"}]

def test_keyed_by_name():
    from broken import status_map
    result = status_map(SERVERS)
    assert "web-01" in result

def test_correct_values():
    from broken import status_map
    result = status_map(SERVERS)
    assert result["web-01"] == "healthy"
    assert result["web-02"] == "down"
