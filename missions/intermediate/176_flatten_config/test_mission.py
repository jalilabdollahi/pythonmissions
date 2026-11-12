import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import broken


CONFIG = {
    "service": {"name": "halcyon", "port": 9100},
    "upstreams": ["10.0.0.1", "10.0.0.2"],
    "labels": {},
    "tags": [],
    "debug": False,
}


def test_nested_dicts_become_dotted_keys():
    flat = broken.flatten(CONFIG)
    assert flat["service.name"] == "halcyon"
    assert flat["service.port"] == 9100


def test_top_level_keys_have_no_leading_separator():
    flat = broken.flatten(CONFIG)
    assert "debug" in flat and flat["debug"] is False
    assert not any(k.startswith(".") for k in flat), "only add the separator when a prefix exists"


def test_list_items_use_their_index():
    flat = broken.flatten(CONFIG)
    assert flat["upstreams.0"] == "10.0.0.1"
    assert flat["upstreams.1"] == "10.0.0.2"


def test_empty_containers_are_kept_as_values():
    flat = broken.flatten(CONFIG)
    assert flat["labels"] == {}
    assert flat["tags"] == []


def test_custom_separator_and_prefix():
    assert broken.flatten({"a": {"b": 1}}, sep="/") == {"a/b": 1}
    assert broken.flatten({"b": 1}, prefix="app") == {"app.b": 1}


def test_lists_of_dicts():
    flat = broken.flatten({"hosts": [{"name": "a"}, {"name": "b"}]})
    assert flat == {"hosts.0.name": "a", "hosts.1.name": "b"}


def test_env_lines_are_sorted_and_uppercase():
    lines = broken.to_env_lines({"service.port": 9100, "debug": False, "upstreams.0": "x"})
    assert lines == ["DEBUG=False", "SERVICE_PORT=9100", "UPSTREAMS_0=x"]


def test_describe_aligns_columns():
    rows = broken.describe({"a": 1, "long.key": 2})
    assert rows == ["a         1", "long.key  2"]
