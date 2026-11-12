import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import broken

CUTOFFS = {"warn": 70, "critical": 85, "page": 95}


def test_levels_between_bounds():
    scale = broken.build_scale(CUTOFFS)
    assert broken.classify(scale, 10) == "ok"
    assert broken.classify(scale, 72) == "warn"
    assert broken.classify(scale, 90) == "critical"
    assert broken.classify(scale, 99) == "page"


def test_value_exactly_on_a_bound_belongs_to_the_higher_level():
    scale = broken.build_scale(CUTOFFS)
    assert broken.classify(scale, 70) == "warn"
    assert broken.classify(scale, 85) == "critical", "lower bounds are inclusive"
    assert broken.classify(scale, 95) == "page"


def test_just_below_a_bound_stays_lower():
    scale = broken.build_scale(CUTOFFS)
    assert broken.classify(scale, 69.9) == "ok"
    assert broken.classify(scale, 94.99) == "critical"


def test_cutoffs_may_be_listed_in_any_order():
    scale = broken.build_scale({"page": 95, "warn": 70, "critical": 85})
    assert broken.classify(scale, 72) == "warn"
    assert broken.classify(scale, 90) == "critical"
    assert broken.classify(scale, 96) == "page"


def test_out_of_range_values_are_rejected():
    scale = broken.build_scale(CUTOFFS)
    with pytest.raises(ValueError):
        broken.classify(scale, -1)
    with pytest.raises(ValueError):
        broken.classify(scale, 100.5)


def test_describe_lists_levels_from_lowest_bound():
    scale = broken.build_scale({"page": 95, "warn": 70, "critical": 85})
    assert broken.describe(scale) == ["warn >= 70%", "critical >= 85%", "page >= 95%"]


def test_escalations_report_only_worse_levels():
    scale = broken.build_scale(CUTOFFS)
    before = {"/a": 60, "/b": 90, "/c": 85}
    after = {"/a": 70, "/b": 80, "/c": 86}
    assert broken.escalations(scale, before, after) == [("/a", "ok", "warn")]


def test_classify_all_and_worst_level():
    scale = broken.build_scale({"page": 95, "warn": 70, "critical": 85})
    volumes = {"/": 50, "/var": 71, "/data": 96}
    assert broken.classify_all(scale, volumes) == {"/": "ok", "/var": "warn", "/data": "page"}
    assert broken.worst_level(scale, volumes) == "page"
