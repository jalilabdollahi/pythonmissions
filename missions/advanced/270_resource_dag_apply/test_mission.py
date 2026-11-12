import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

from broken import CycleError, MissingDependency, apply_all, describe, destroy_all, levels

STACK = {
    "vpc": [],
    "subnet": ["vpc"],
    "sg": ["vpc"],
    "db": ["subnet", "sg"],
    "cache": ["subnet"],
    "app": ["db", "cache", "vpc"],
}


def test_independent_resources_share_a_level():
    assert levels(STACK) == [["vpc"], ["sg", "subnet"], ["cache", "db"], ["app"]]


def test_resource_goes_above_its_deepest_dependency():
    graph = {"a": [], "b": ["a"], "c": ["b"], "d": ["a", "c"]}
    assert levels(graph) == [["a"], ["b"], ["c"], ["d"]], "d needs c, so it cannot run beside b"


def test_cycles_are_reported_with_their_path():
    graph = {"a": ["b"], "b": ["c"], "c": ["a"], "d": []}
    with pytest.raises(CycleError) as info:
        levels(graph)
    assert set(info.value.path) == {"a", "b", "c"}
    assert info.value.path[0] == info.value.path[-1]


def test_unknown_dependency_is_an_error_not_silently_ignored():
    with pytest.raises(MissingDependency):
        levels({"app": ["ghost"]})


def test_apply_runs_dependencies_first():
    order = []
    status, attempted = apply_all(STACK, order.append)
    assert set(status.values()) == {"ok"}
    assert order.index("vpc") < order.index("subnet") < order.index("db") < order.index("app")
    assert attempted == [["vpc"], ["sg", "subnet"], ["cache", "db"], ["app"]]


def test_destroy_runs_in_reverse_so_dependents_go_first():
    order = []
    destroy_all(STACK, order.append)
    assert order[0] == "app" and order[-1] == "vpc"
    assert order.index("db") < order.index("subnet"), "the database lives in the subnet"
    assert order.index("cache") < order.index("subnet")


def test_failure_blocks_everything_downstream_transitively():
    def action(name):
        if name == "subnet":
            raise RuntimeError("quota")

    status, attempted = apply_all(STACK, action)
    assert status["subnet"] == "failed"
    assert status["sg"] == "ok", "unrelated branches still apply"
    assert status["db"] == "skipped" and status["cache"] == "skipped"
    assert status["app"] == "skipped", "app is two hops from the failure and must not run either"
    assert attempted[-1] == []


def test_failed_delete_protects_what_it_depends_on():
    def action(name):
        if name == "db":
            raise RuntimeError("deletion protection")

    status, _ = destroy_all(STACK, action)
    assert status["db"] == "failed"
    assert status["subnet"] == "skipped", "cannot delete a subnet that still hosts a database"
    assert status["sg"] == "skipped"
    assert status["cache"] == "ok"
    assert status["vpc"] == "skipped"
    assert describe({"x": [], "y": ["x"]}) == ["level 0: x", "level 1: y"]
