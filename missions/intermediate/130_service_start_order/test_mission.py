import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import broken


def test_dependencies_come_first():
    order = broken.start_order({"api": ["db", "cache"], "worker": ["api"]})
    assert order.index("db") < order.index("api")
    assert order.index("cache") < order.index("api")
    assert order.index("api") < order.index("worker")


def test_leaf_services_only_seen_as_dependencies_are_included():
    order = broken.start_order({"api": ["db"]})
    assert order == ["db", "api"], "db appears only as a dependency but must still be started"


def test_ties_are_alphabetical():
    order = broken.start_order({"web": [], "auth": [], "mail": [], "app": ["web", "auth"]})
    assert order == ["auth", "mail", "web", "app"]


def test_independent_services_listed():
    assert broken.start_order({"b": [], "a": []}) == ["a", "b"]


def test_cycle_raises_value_error():
    with pytest.raises(ValueError) as info:
        broken.start_order({"a": ["b"], "b": ["a"], "c": []})
    assert "cycle" in str(info.value)
    assert "a" in str(info.value)


def test_self_dependency_is_a_cycle():
    with pytest.raises(ValueError):
        broken.start_order({"a": ["a"]})


def test_shutdown_is_reverse_of_start():
    deps = {"api": ["db"], "web": ["api"]}
    assert broken.shutdown_order(deps) == ["web", "api", "db"]
