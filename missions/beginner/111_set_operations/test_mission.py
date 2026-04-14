import os, sys
sys.path.insert(0, os.path.dirname(__file__))

def test_common_only():
    from broken import common_failures
    result = common_failures({"web-01","web-02","db-01"}, {"web-02","db-01","api-01"})
    assert result == {"web-02", "db-01"}

def test_no_common():
    from broken import common_failures
    assert common_failures({"web-01"}, {"db-01"}) == set()

def test_all_common():
    from broken import common_failures
    assert common_failures({"a","b"}, {"a","b"}) == {"a","b"}
