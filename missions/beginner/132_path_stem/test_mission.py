import os, sys
sys.path.insert(0, os.path.dirname(__file__))

def test_strips_extension():
    from broken import get_config_name
    assert get_config_name("/etc/myapp/database.yaml") == "database"

def test_no_extension_included():
    from broken import get_config_name
    result = get_config_name("/etc/myapp/config.json")
    assert "." not in result
