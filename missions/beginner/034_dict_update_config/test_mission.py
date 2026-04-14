import os, sys
sys.path.insert(0, os.path.dirname(__file__))

def test_override_applied():
    from broken import merge_config
    result = merge_config({"port": 5432}, {"port": 5433})
    assert result["port"] == 5433

def test_new_keys_added():
    from broken import merge_config
    result = merge_config({"host": "localhost"}, {"debug": True})
    assert result["debug"] is True

def test_base_keys_kept():
    from broken import merge_config
    result = merge_config({"host": "localhost", "port": 5432}, {"port": 5433})
    assert result["host"] == "localhost"

def test_base_not_mutated():
    from broken import merge_config
    base = {"port": 5432}
    merge_config(base, {"port": 5433})
    assert base["port"] == 5432
