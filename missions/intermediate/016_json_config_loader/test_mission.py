import pytest
import sys
import json
sys.path.insert(0, ".")
from broken import load_config, get_setting

def test_load_config(tmp_path):
    cfg = tmp_path / "config.json"
    cfg.write_text(json.dumps({"port": 8080, "host": "localhost"}))
    result = load_config(str(cfg))
    assert result["port"] == 8080

def test_get_setting():
    config = {"port": 8080}
    assert get_setting(config, "port") == 8080
    assert get_setting(config, "timeout", 30) == 30
