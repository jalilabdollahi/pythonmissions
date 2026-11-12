import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import json

import pytest

from broken import DEFAULTS, describe, load_settings


def test_missing_file_returns_defaults(tmp_path):
    assert load_settings(tmp_path / "local.json") == {"timeout": 30, "retries": 3, "region": "eu-west"}


def test_overrides_replace_defaults(tmp_path):
    path = tmp_path / "local.json"
    path.write_text(json.dumps({"timeout": 5}), encoding="utf-8")
    assert load_settings(path) == {"timeout": 5, "retries": 3, "region": "eu-west"}, "unset keys keep their defaults"


def test_overrides_do_not_leak_into_defaults(tmp_path):
    path = tmp_path / "local.json"
    path.write_text(json.dumps({"region": "us-east"}), encoding="utf-8")
    load_settings(path)
    assert DEFAULTS["region"] == "eu-west", "DEFAULTS must never be modified"
    assert load_settings(tmp_path / "other.json")["region"] == "eu-west"


def test_invalid_json_is_not_hidden(tmp_path):
    path = tmp_path / "local.json"
    path.write_text("{not json", encoding="utf-8")
    with pytest.raises(ValueError):
        load_settings(path)


def test_describe_is_sorted():
    assert describe({"b": 1, "a": 2}) == "a=2, b=1"
