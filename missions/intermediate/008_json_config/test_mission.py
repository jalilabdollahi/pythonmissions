import json
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(__file__))


@pytest.fixture
def config_file(tmp_path):
    return str(tmp_path / "config.json")


def test_load_returns_empty_for_missing_file(tmp_path):
    from broken import load_config
    result = load_config(str(tmp_path / "nonexistent.json"))
    assert result == {}


def test_save_creates_file(config_file):
    from broken import save_config
    save_config(config_file, {"key": "value"})
    assert os.path.exists(config_file)


def test_save_writes_valid_json(config_file):
    from broken import save_config
    data = {"env": "staging", "replicas": 3}
    save_config(config_file, data)
    with open(config_file) as f:
        loaded = json.load(f)
    assert loaded == data


def test_load_reads_saved_data(config_file):
    from broken import save_config, load_config
    original = {"service": "api", "port": 8080}
    save_config(config_file, original)
    loaded = load_config(config_file)
    assert loaded == original


def test_update_config_merges(config_file):
    from broken import load_config, save_config, update_config
    save_config(config_file, {"a": 1, "b": 2})
    result = update_config(config_file, {"b": 99, "c": 3})
    assert result["a"] == 1
    assert result["b"] == 99
    assert result["c"] == 3


def test_roundtrip_preserves_types(config_file):
    from broken import load_config, save_config
    data = {"flag": True, "count": 42, "name": "test", "items": [1, 2, 3]}
    save_config(config_file, data)
    loaded = load_config(config_file)
    assert loaded == data
