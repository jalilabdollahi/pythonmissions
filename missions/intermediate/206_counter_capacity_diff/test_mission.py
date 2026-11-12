import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from collections import Counter

import broken

HAVE = {"m5.large": 4, "c5.xlarge": 2, "t3.small": 3}
WANT = {"m5.large": 6, "t3.small": 3, "r5.large": 1}


def test_shortages_are_reported_as_to_add():
    to_add, _ = broken.capacity_diff(Counter(HAVE), Counter(WANT))
    assert to_add == {"m5.large": 2, "r5.large": 1}, "Counter - Counter drops what is missing"


def test_surplus_is_reported_as_to_remove():
    _, to_remove = broken.capacity_diff(Counter(HAVE), Counter(WANT))
    assert to_remove == {"c5.xlarge": 2}


def test_arguments_are_not_modified():
    have, want = Counter(HAVE), Counter(WANT)
    broken.capacity_diff(have, want)
    assert have == Counter(HAVE)
    assert want == Counter(WANT)


def test_identical_fleets_need_nothing():
    assert broken.capacity_diff(Counter(HAVE), Counter(HAVE)) == ({}, {})


def test_total_counts_instances_not_types():
    assert broken.total_instances(Counter(HAVE)) == 9


def test_headroom_rounds_up():
    result = broken.with_headroom(Counter({"m5.large": 4, "t3.small": 1}), 25)
    assert result == Counter({"m5.large": 5, "t3.small": 2})
    assert broken.with_headroom(Counter({"a": 3}), 10)["a"] == 4


def test_biggest_surplus_and_utilisation():
    assert broken.biggest_surplus(Counter(HAVE), Counter(WANT), 1) == [("c5.xlarge", 2)]
    assert broken.utilisation(Counter(HAVE), Counter(WANT)) == 1.11
    assert broken.utilisation(Counter(), Counter(WANT)) == 0.0


def test_plan_summary_lines():
    lines = broken.plan_summary(Counter(HAVE), Counter(WANT))
    assert lines == ["add 2 x m5.large", "add 1 x r5.large", "remove 2 x c5.xlarge"]
    assert broken.plan_summary(Counter(HAVE), Counter(HAVE)) == ["no changes"]
