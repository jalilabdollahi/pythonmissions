import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import ordered_builds, latest_build, builds_after


def test_numeric_order():
    assert ordered_builds(["10", "9", "100", "8"]) == ["8", "9", "10", "100"], "compare numbers, not characters"


def test_items_stay_strings():
    assert all(isinstance(b, str) for b in ordered_builds(["2", "1"]))


def test_latest_build_after_the_counter_gains_a_digit():
    assert latest_build(["98", "99", "100"]) == "100"


def test_latest_of_empty_is_none():
    assert latest_build([]) is None


def test_builds_after_returns_newer_in_order():
    assert builds_after(["120", "99", "101", "100"], "100") == ["101", "120"]
