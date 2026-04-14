import os, sys
sys.path.insert(0, os.path.dirname(__file__))

def test_correct_merge():
    from broken import merge
    result = merge({"host": "localhost", "port": 5432}, {"port": 5433, "debug": True})
    assert result["port"] == 5433
    assert result["host"] == "localhost"

def test_base_not_modified():
    from broken import merge
    base = {"host": "localhost", "port": 5432}
    merge(base, {"port": 5433})
    assert base["port"] == 5432
