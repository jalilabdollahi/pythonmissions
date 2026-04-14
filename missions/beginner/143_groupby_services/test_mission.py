import os, sys
sys.path.insert(0, os.path.dirname(__file__))

DEPS = [
    {"service":"web","version":"1.2"},
    {"service":"api","version":"2.0"},
    {"service":"web","version":"1.3"},
]

def test_groups_web():
    from broken import group_by_service
    result = group_by_service(DEPS)
    assert len(result["web"]) == 2

def test_groups_api():
    from broken import group_by_service
    result = group_by_service(DEPS)
    assert len(result["api"]) == 1
