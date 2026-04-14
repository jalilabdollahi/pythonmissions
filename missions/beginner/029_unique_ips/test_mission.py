import os, sys
sys.path.insert(0, os.path.dirname(__file__))

def test_removes_duplicates():
    from broken import unique_ips
    result = unique_ips(["10.0.0.1", "10.0.0.2", "10.0.0.1"])
    assert len(result) == 2

def test_all_present():
    from broken import unique_ips
    result = unique_ips(["10.0.0.1", "10.0.0.2", "10.0.0.1"])
    assert "10.0.0.1" in result
    assert "10.0.0.2" in result

def test_no_duplicates_unchanged():
    from broken import unique_ips
    result = unique_ips(["10.0.0.1", "10.0.0.2"])
    assert len(result) == 2
