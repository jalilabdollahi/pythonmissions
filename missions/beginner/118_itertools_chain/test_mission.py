import os, sys
sys.path.insert(0, os.path.dirname(__file__))

def test_flat_result():
    from broken import chain_logs
    result = chain_logs([["a","b"],["c","d"],["e"]])
    assert result == ["a","b","c","d","e"]

def test_no_nested_lists():
    from broken import chain_logs
    result = chain_logs([["a"],["b"]])
    for item in result:
        assert isinstance(item, str)
