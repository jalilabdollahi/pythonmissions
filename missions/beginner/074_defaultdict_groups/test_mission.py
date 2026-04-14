import os, sys
sys.path.insert(0, os.path.dirname(__file__))

SERVERS = [
    {"name": "web-01", "region": "us-east"},
    {"name": "web-02", "region": "eu-west"},
    {"name": "web-03", "region": "us-east"},
]

def test_returns_dict():
    from broken import group_by_region
    assert isinstance(group_by_region(SERVERS), dict)

def test_correct_groups():
    from broken import group_by_region
    result = group_by_region(SERVERS)
    assert "web-01" in result["us-east"]
    assert "web-03" in result["us-east"]
    assert "web-02" in result["eu-west"]
