import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import TOMBSTONE, LsmTree, get_from_runs, merge_runs


def test_merge_is_sorted_with_one_entry_per_key():
    newer = [("b", 2), ("d", 4)]
    older = [("a", 1), ("c", 3), ("e", 5)]
    assert merge_runs([newer, older], last_level=True) == [("a", 1), ("b", 2), ("c", 3), ("d", 4), ("e", 5)]


def test_newest_value_wins_on_duplicate_keys():
    newest, middle, oldest = [("k", "v3")], [("k", "v2")], [("k", "v1")]
    assert merge_runs([newest, middle, oldest], last_level=True) == [("k", "v3")]
    assert merge_runs([middle, oldest], last_level=False) == [("k", "v2")]


def test_tombstone_shadows_older_value_in_the_merge():
    newer = [("gone", TOMBSTONE), ("x", 2)]
    older = [("gone", "old"), ("x", 1)]
    merged = merge_runs([newer, older], last_level=False)
    assert merged == [("gone", TOMBSTONE), ("x", 2)], "the tombstone must survive: deeper runs may still hold the key"


def test_tombstones_are_dropped_only_at_the_last_level():
    runs = [[("gone", TOMBSTONE), ("x", 2)], [("gone", "old")]]
    assert merge_runs(runs, last_level=True) == [("x", 2)]
    assert [k for k, v in merge_runs(runs, last_level=False) if v is TOMBSTONE] == ["gone"]


def test_get_treats_a_tombstone_as_deleted_not_as_missing():
    runs = [[("k", TOMBSTONE)], [("k", "stale")]]
    assert get_from_runs(runs, "k") is None, "must not fall through to the older version"
    assert get_from_runs([[("k", "v")]], "k") == "v"
    assert get_from_runs([[("k", "v")]], "other") is None


def test_tree_delete_survives_flush_and_compaction():
    tree = LsmTree(level0_limit=2)
    tree.put("a", 1)
    tree.put("b", 2)
    tree.flush()
    tree.delete("a")
    tree.put("c", 3)
    tree.flush()
    assert tree.get("a") is None and tree.get("b") == 2 and tree.get("c") == 3
    assert tree.items() == [("b", 2), ("c", 3)]


def test_full_compaction_removes_tombstones_physically():
    tree = LsmTree(level0_limit=2)
    tree.put("a", 1)
    tree.flush()
    tree.delete("a")
    tree.flush()
    assert tree.level0 == [] and tree.level1 == [], "nothing is left to shadow, so the tombstone is dropped"


def test_overwrites_keep_the_latest_version_after_compaction():
    tree = LsmTree(level0_limit=3)
    for version in ("v1", "v2", "v3"):
        tree.put("cfg", version)
        tree.flush()
    assert tree.get("cfg") == "v3"
    assert tree.level1 == [("cfg", "v3")]
