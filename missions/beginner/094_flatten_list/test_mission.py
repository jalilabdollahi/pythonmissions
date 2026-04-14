import os, sys
sys.path.insert(0, os.path.dirname(__file__))

def test_flat_result():
    from broken import flatten
    result = flatten([["web-01","web-02"],["db-01"]])
    assert result == ["web-01", "web-02", "db-01"]

def test_no_nested_lists():
    from broken import flatten
    result = flatten([["a"],["b","c"]])
    for item in result:
        assert isinstance(item, str)

def test_empty_inner():
    from broken import flatten
    assert flatten([[], ["web-01"]]) == ["web-01"]
