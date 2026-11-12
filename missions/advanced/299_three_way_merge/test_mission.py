import copy
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import MergeConflict, changed_paths, merge_strict, three_way_merge


BASE = {"service": {"timeout": 30, "pool": {"size": 5, "idle": 60}}, "debug": False}


def test_independent_changes_in_the_same_section_merge_cleanly():
    ours = copy.deepcopy(BASE)
    ours["service"]["timeout"] = 10
    theirs = copy.deepcopy(BASE)
    theirs["service"]["pool"]["size"] = 20
    merged, conflicts = three_way_merge(BASE, ours, theirs)
    assert conflicts == [], "different keys inside one block are not a conflict"
    assert merged["service"] == {"timeout": 10, "pool": {"size": 20, "idle": 60}}


def test_conflict_reports_the_full_dotted_path_and_keeps_ours():
    ours = copy.deepcopy(BASE)
    ours["service"]["pool"]["size"] = 8
    theirs = copy.deepcopy(BASE)
    theirs["service"]["pool"]["size"] = 12
    merged, conflicts = three_way_merge(BASE, ours, theirs)
    assert conflicts == ["service.pool.size"]
    assert merged["service"]["pool"]["size"] == 8


def test_same_change_on_both_sides_is_not_a_conflict():
    ours = copy.deepcopy(BASE)
    theirs = copy.deepcopy(BASE)
    ours["debug"] = theirs["debug"] = True
    assert three_way_merge(BASE, ours, theirs) == (dict(BASE, debug=True), [])


def test_deletion_is_not_the_same_as_null():
    base = {"proxy": None, "mode": "a"}
    ours = {"mode": "a"}  # deleted proxy
    theirs = {"proxy": None, "mode": "b"}
    merged, conflicts = three_way_merge(base, ours, theirs)
    assert "proxy" not in merged, "ours deleted it and theirs left it alone"
    assert merged["mode"] == "b" and conflicts == []


def test_delete_versus_modify_is_a_conflict():
    base = {"a": 1}
    merged, conflicts = three_way_merge(base, {}, {"a": 2})
    assert conflicts == ["a"]
    assert merged == {}


def test_added_key_with_different_values_conflicts_but_same_value_does_not():
    merged, conflicts = three_way_merge({}, {"x": 1, "y": 2}, {"x": 1, "y": 3})
    assert conflicts == ["y"]
    assert merged["x"] == 1


def test_merge_does_not_alias_or_mutate_inputs():
    base = {"hosts": ["a"]}
    ours = {"hosts": ["a"], "extra": {"tags": ["x"]}}
    theirs = {"hosts": ["a", "b"]}
    snapshot = copy.deepcopy((base, ours, theirs))
    merged, _ = three_way_merge(base, ours, theirs)
    merged["hosts"].append("c")
    merged["extra"]["tags"].append("y")
    assert (base, ours, theirs) == snapshot, "inputs must stay untouched"


def test_strict_merge_and_review_helpers():
    ours = dict(BASE, debug=True)
    assert merge_strict(BASE, ours, BASE)["debug"] is True
    assert changed_paths(BASE, {"service": {"timeout": 1, "pool": {"size": 5, "idle": 60}}, "debug": False}) == ["service.timeout"]
    try:
        merge_strict({"a": 1}, {"a": 2}, {"a": 3})
    except MergeConflict as exc:
        assert exc.paths == ["a"]
    else:
        raise AssertionError("strict merge must raise on conflicts")
