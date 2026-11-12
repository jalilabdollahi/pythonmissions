import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import group_by_region, region_sizes, largest_region, report

HOSTS = [("a1", "eu-west"), ("b1", "us-east"), ("a2", "eu-west"), ("a3", "eu-west"), ("c1", "ap-south")]


def test_group_by_region_collects_all_hosts():
    assert group_by_region(HOSTS)["eu-west"] == ["a1", "a2", "a3"], "a new region needs an empty list first"


def test_group_by_region_has_every_region():
    assert set(group_by_region(HOSTS)) == {"eu-west", "us-east", "ap-south"}


def test_group_by_region_empty_input():
    assert group_by_region([]) == {}


def test_result_is_a_normal_dict_for_missing_keys():
    groups = group_by_region(HOSTS)
    assert "mars-1" not in groups


def test_region_sizes():
    assert region_sizes(HOSTS) == {"eu-west": 3, "us-east": 1, "ap-south": 1}


def test_largest_region():
    assert largest_region(HOSTS) == "eu-west"
    assert largest_region([]) is None


def test_report_is_sorted_by_region():
    assert report(HOSTS) == ["ap-south: c1", "eu-west: a1, a2, a3", "us-east: b1"]
