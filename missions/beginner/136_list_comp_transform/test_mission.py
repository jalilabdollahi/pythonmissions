import os, sys
sys.path.insert(0, os.path.dirname(__file__))

ENDPOINTS = [
    {"hostname": "web-01.internal", "port": 80},
    {"hostname": "api-01.internal", "port": 8080},
]

def test_returns_hostnames():
    from broken import get_hostnames
    result = get_hostnames(ENDPOINTS)
    assert result == ["web-01.internal", "api-01.internal"]

def test_count():
    from broken import get_hostnames
    assert len(get_hostnames(ENDPOINTS)) == 2
