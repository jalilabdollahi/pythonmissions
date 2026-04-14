import os, sys
sys.path.insert(0, os.path.dirname(__file__))

NODES = [
    {"name": "node-01", "status": "active"},
    {"name": "node-02", "status": "inactive"},
    {"name": "node-03", "status": "active"},
    {"name": "node-04", "status": "shutdown"},
    {"name": "node-05", "status": "active"},
]

def test_includes_active():
    from broken import report_nodes
    result = report_nodes(NODES)
    assert "node-01" in result
    assert "node-03" in result

def test_excludes_inactive():
    from broken import report_nodes
    result = report_nodes(NODES)
    assert "node-02" not in result

def test_stops_at_shutdown():
    from broken import report_nodes
    result = report_nodes(NODES)
    assert "node-05" not in result
