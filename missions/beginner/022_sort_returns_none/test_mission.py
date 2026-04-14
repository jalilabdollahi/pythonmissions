import os, sys
sys.path.insert(0, os.path.dirname(__file__))

def test_returns_list():
    from broken import sorted_hosts
    assert sorted_hosts(["c", "a", "b"]) is not None

def test_sorted_order():
    from broken import sorted_hosts
    assert sorted_hosts(["web-03", "web-01", "web-02"]) == ["web-01", "web-02", "web-03"]

def test_does_not_modify_original():
    from broken import sorted_hosts
    original = ["web-03", "web-01"]
    sorted_hosts(original)
    assert original == ["web-03", "web-01"]
