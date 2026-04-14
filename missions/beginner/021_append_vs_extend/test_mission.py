import os, sys
sys.path.insert(0, os.path.dirname(__file__))

def test_flat_result():
    from broken import merge_servers
    result = merge_servers(["web-01", "web-02"], ["web-03", "web-04"])
    assert result == ["web-01", "web-02", "web-03", "web-04"]

def test_no_nested_list():
    from broken import merge_servers
    result = merge_servers(["a"], ["b", "c"])
    for item in result:
        assert isinstance(item, str)

def test_empty_new():
    from broken import merge_servers
    assert merge_servers(["web-01"], []) == ["web-01"]

def test_does_not_modify_original():
    from broken import merge_servers
    base = ["web-01"]
    merge_servers(base, ["web-02"])
    assert base == ["web-01"]
