import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import run_checks, verdict


def passing():
    return True


def failing():
    return False


def test_all_passing_checks_count_zero():
    assert run_checks({"login": passing, "pay": passing}) == 0


def test_failures_are_counted():
    assert run_checks({"login": failing, "pay": passing, "search": failing}) == 2


def test_each_run_starts_from_zero():
    checks = {"login": failing, "pay": failing}
    assert run_checks(checks) == 2
    assert run_checks(checks) == 2, "a second run must not remember the first"


def test_empty_checks_count_zero():
    assert run_checks({}) == 0


def test_verdict_rolls_back_on_two_failures():
    assert verdict({"a": failing, "b": failing}) == "rollback"


def test_verdict_ships_on_single_failure():
    assert verdict({"a": failing, "b": passing}) == "ship"
