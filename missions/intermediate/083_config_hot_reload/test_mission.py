import pytest, sys, json, time
sys.path.insert(0, ".")
from broken import HotConfig

def test_get_value(tmp_path):
    cfg_file = tmp_path / "config.json"
    cfg_file.write_text(json.dumps({"env": "prod", "port": 8080}))
    hc = HotConfig(str(cfg_file))
    assert hc.get("env") == "prod"

def test_reload_on_change(tmp_path):
    cfg_file = tmp_path / "config.json"
    cfg_file.write_text(json.dumps({"version": "v1"}))
    hc = HotConfig(str(cfg_file))
    hc.get("version")
    time.sleep(0.05)
    cfg_file.write_text(json.dumps({"version": "v2"}))
    import os
    os.utime(str(cfg_file), (time.time() + 1, time.time() + 1))
    assert hc.get("version") == "v2"
