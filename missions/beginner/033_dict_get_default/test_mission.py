import os, sys
sys.path.insert(0, os.path.dirname(__file__))

def test_existing_key():
    from broken import get_config
    cfg = {"host": "localhost", "port": 5432}
    assert get_config(cfg, "host", "unknown") == "localhost"

def test_missing_key_default():
    from broken import get_config
    cfg = {"host": "localhost"}
    assert get_config(cfg, "timeout", 30) == 30

def test_missing_key_none_default():
    from broken import get_config
    assert get_config({}, "key") is None
