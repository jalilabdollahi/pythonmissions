import copy
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import broken

DEFAULTS = {
    "database": {"host": "db.internal", "port": 5432, "pool": {"min": 1, "max": 10}},
    "debug": False,
}


def test_nested_siblings_survive():
    merged = broken.deep_merge(DEFAULTS, {"database": {"host": "db.staging"}})
    assert merged["database"]["host"] == "db.staging"
    assert merged["database"]["port"] == 5432, "keys not mentioned in the override must be kept"


def test_two_levels_deep():
    merged = broken.deep_merge(DEFAULTS, {"database": {"pool": {"max": 50}}})
    assert merged["database"]["pool"] == {"min": 1, "max": 50}


def test_none_removes_a_key():
    merged = broken.deep_merge(DEFAULTS, {"debug": None, "database": {"port": None}})
    assert "debug" not in merged
    assert "port" not in merged["database"]


def test_inputs_are_not_modified():
    base = copy.deepcopy(DEFAULTS)
    override = {"database": {"pool": {"max": 50}}}
    snapshot = copy.deepcopy(override)
    merged = broken.deep_merge(base, override)
    merged["database"]["pool"]["min"] = 99
    assert base == DEFAULTS
    assert override == snapshot


def test_lists_are_replaced_not_merged():
    merged = broken.deep_merge({"hosts": ["a", "b"]}, {"hosts": ["c"]})
    assert merged["hosts"] == ["c"]


def test_last_layer_wins():
    cfg = broken.build_config({"mode": "base", "x": 1}, {"mode": "prod"}, {"mode": "hotfix"})
    assert cfg == {"mode": "hotfix", "x": 1}


def test_flatten_dotted_keys():
    flat = broken.flatten({"a": {"b": 1, "c": {"d": 2}}, "e": 3})
    assert flat == {"a.b": 1, "a.c.d": 2, "e": 3}
