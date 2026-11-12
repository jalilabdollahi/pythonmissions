import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import broken
from broken import apply_plan, bucket_of, build_tree, diff_buckets, diff_keys, leaf_hash, repair_plan, root_hash


def key_in_bucket(bucket, prefix="user"):
    for i in range(10000):
        key = f"{prefix}-{i}"
        if bucket_of(key) == bucket:
            return key
    raise AssertionError("no key found")


def test_same_contents_same_root_regardless_of_insertion_order():
    a = {"x": "1", "y": "2", "z": "3"}
    b = {"z": "3", "x": "1", "y": "2"}
    assert root_hash(a) == root_hash(b), "hash input must be canonical (sorted)"
    assert leaf_hash([("a", "1"), ("b", "2")]) == leaf_hash([("b", "2"), ("a", "1")])


def test_field_boundaries_are_part_of_the_hash():
    assert leaf_hash([("a", "bc")]) != leaf_hash([("ab", "c")]), "need a delimiter between key and value"
    assert leaf_hash([("a", "1"), ("b", "2")]) != leaf_hash([("a", "1b"), ("", "2")])


def test_tree_shape_and_identical_stores_have_no_diff():
    tree = build_tree({"k": "v"})
    assert [len(level) for level in tree] == [8, 4, 2, 1]
    assert diff_buckets(tree, build_tree({"k": "v"})) == []


def test_single_difference_is_located_in_its_bucket():
    k = key_in_bucket(5)
    a = {k: "old", "other": "same"}
    b = {k: "new", "other": "same"}
    assert diff_buckets(build_tree(a), build_tree(b)) == [bucket_of(k)]
    assert diff_keys(a, b) == [k]


def test_differences_in_both_halves_of_the_tree_are_found():
    left, right = key_in_bucket(1), key_in_bucket(6)
    a = {left: "1", right: "1"}
    b = {left: "2", right: "2"}
    assert diff_buckets(build_tree(a), build_tree(b)) == [1, 6], "walk must visit every differing child"
    assert diff_keys(a, b) == sorted([left, right])


def test_keys_missing_on_either_side_are_reported():
    only_a, only_b = key_in_bucket(2, "a"), key_in_bucket(3, "b")
    a = {only_a: "1", "shared": "s"}
    b = {only_b: "2", "shared": "s"}
    assert diff_keys(a, b) == sorted([only_a, only_b])
    assert diff_keys({}, b) == sorted([only_b, "shared"])


def test_repair_plan_converges_replicas():
    source = {"a": "1", "b": "2", "c": "3"}
    target = {"a": "1", "b": "stale", "d": "orphan"}
    plan = repair_plan(source, target)
    assert plan["copy"] == {"b": "2", "c": "3"}
    assert plan["delete"] == ["d"]
    assert apply_plan(target, plan) == source
    assert root_hash(target) == root_hash(source)
