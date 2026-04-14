import os, sys
sys.path.insert(0, os.path.dirname(__file__))

def test_sorted_by_key():
    from broken import sorted_config
    cfg = {"port": "5432", "host": "localhost", "db": "myapp"}
    result = sorted_config(cfg)
    keys = [k for k, v in result]
    assert keys == sorted(keys)

def test_returns_tuples():
    from broken import sorted_config
    result = sorted_config({"a": "1"})
    assert isinstance(result[0], tuple)
