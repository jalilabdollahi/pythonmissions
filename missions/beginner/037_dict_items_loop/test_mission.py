import os, sys
sys.path.insert(0, os.path.dirname(__file__))

def test_formats_correctly():
    from broken import print_config
    result = print_config({"host": "localhost"})
    assert "host=localhost" in result

def test_all_keys_present():
    from broken import print_config
    cfg = {"host": "localhost", "port": "5432"}
    result = print_config(cfg)
    assert len(result) == 2

def test_values_included():
    from broken import print_config
    result = print_config({"timeout": "30"})
    assert result[0] == "timeout=30"
