import os
import sys
from datetime import datetime

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import broken


def test_star_and_number():
    assert broken.field_matches("*", 17, 0, 59)
    assert broken.field_matches("15", 15, 0, 59)
    assert not broken.field_matches("15", 16, 0, 59)


def test_range_is_inclusive_on_both_ends():
    assert broken.field_matches("1-5", 1, 0, 59)
    assert broken.field_matches("1-5", 5, 0, 59), "cron ranges include the last number"
    assert not broken.field_matches("1-5", 6, 0, 59)


def test_comma_list_matches_any_member():
    assert broken.field_matches("0,30", 30, 0, 59)
    assert broken.field_matches("0,30", 0, 0, 59)
    assert not broken.field_matches("0,30", 15, 0, 59)


def test_list_of_ranges_and_numbers():
    assert broken.field_matches("1-3,10,20-22", 21, 0, 59)
    assert not broken.field_matches("1-3,10,20-22", 11, 0, 59)


def test_star_step_from_zero():
    assert broken.field_matches("*/15", 45, 0, 59)
    assert not broken.field_matches("*/15", 20, 0, 59)


def test_star_step_counts_from_range_start():
    assert broken.field_matches("*/2", 1, 1, 31), "day-of-month steps start at 1"
    assert broken.field_matches("*/2", 3, 1, 31)
    assert not broken.field_matches("*/2", 2, 1, 31)


def test_range_step_starts_at_range_start():
    assert broken.field_matches("7-30/10", 17, 0, 59)
    assert broken.field_matches("7-30/10", 7, 0, 59)
    assert not broken.field_matches("7-30/10", 20, 0, 59), "steps count from 7, not from 0"


def test_full_expression_with_weekday():
    monday_nine = datetime(2025, 3, 3, 9, 30)
    assert broken.cron_matches("30 9 * * 1", monday_nine)
    assert not broken.cron_matches("30 9 * * 0", monday_nine)
    with pytest.raises(ValueError):
        broken.cron_matches("* * *", monday_nine)
