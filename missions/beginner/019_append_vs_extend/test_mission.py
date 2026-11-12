import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import merge_regions, host_count, patch_targets

INVENTORY = {"us": ["u1.willow.io", "u2.willow.io"], "eu": ["e1.willow.io"], "ap": []}


def test_merged_list_is_flat():
    merged = merge_regions(INVENTORY)
    assert all(isinstance(h, str) for h in merged), "each host must be its own element"


def test_regions_sorted_hosts_in_original_order():
    assert merge_regions(INVENTORY) == ["e1.willow.io", "u1.willow.io", "u2.willow.io"]


def test_host_count_counts_hosts_not_regions():
    assert host_count(INVENTORY) == 3


def test_empty_inventory():
    assert merge_regions({}) == []


def test_patch_targets_filter_by_suffix():
    inv = {"us": ["a.canary", "b.stable"], "eu": ["c.canary"]}
    assert patch_targets(inv, ".canary") == ["c.canary", "a.canary"]
