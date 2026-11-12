import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import broken


def test_added_and_removed_keys():
    d = broken.diff_configs({"a": 1, "b": 2}, {"b": 2, "c": 3})
    assert d["added"] == {"c": 3}
    assert d["removed"] == {"a": 1}
    assert d["changed"] == {}


def test_changed_value_reports_old_and_new():
    d = broken.diff_configs({"timeout": 30}, {"timeout": 60})
    assert d["changed"] == {"timeout": (30, 60)}


def test_falsy_old_value_is_not_missing():
    d = broken.diff_configs({"retries": 0, "name": ""}, {"retries": 3, "name": "x"})
    assert d["added"] == {}, "retries exists with value 0, so it was not added"
    assert d["changed"] == {"retries": (0, 3), "name": ("", "x")}


def test_equal_lists_are_not_a_change():
    old = {"hosts": ["a", "b"]}
    new = {"hosts": ["a", "b"]}
    assert broken.diff_configs(old, new)["changed"] == {}, "compare with ==, not identity"
    assert broken.is_clean(broken.diff_configs(old, new))


def test_is_clean_false_when_anything_differs():
    assert not broken.is_clean(broken.diff_configs({}, {"x": 1}))


def test_summary_is_sorted_within_sections():
    d = broken.diff_configs({"z": 1, "y": 2, "m": 1}, {"b": 1, "a": 2, "m": 5})
    assert broken.summarize(d).splitlines() == ["+ a=2", "+ b=1", "- y=2", "- z=1", "~ m: 1 -> 5"]


def test_summary_of_identical_configs():
    assert broken.summarize(broken.diff_configs({"a": 1}, {"a": 1})) == "no differences"
