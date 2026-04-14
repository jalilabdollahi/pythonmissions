import os, sys
sys.path.insert(0, os.path.dirname(__file__))

def test_joins_path():
    from broken import config_path
    result = config_path("/etc/myapp", "config.yaml")
    assert result == os.path.join("/etc/myapp", "config.yaml")

def test_no_double_slash():
    from broken import config_path
    result = config_path("/etc/myapp/", "config.yaml")
    assert "//" not in result
