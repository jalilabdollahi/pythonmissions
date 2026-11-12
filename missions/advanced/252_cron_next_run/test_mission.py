import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

from broken import CronSpec, next_run, upcoming


def nxt(expr, after):
    return next_run(CronSpec(expr), after)


def test_result_is_strictly_after_the_reference_time():
    assert nxt("30 10 * * *", datetime(2025, 3, 3, 10, 30, 0)) == datetime(2025, 3, 4, 10, 30)
    assert nxt("30 10 * * *", datetime(2025, 3, 3, 10, 30, 45)) == datetime(2025, 3, 4, 10, 30)
    assert nxt("30 10 * * *", datetime(2025, 3, 3, 10, 29, 59)) == datetime(2025, 3, 3, 10, 30)


def test_step_expressions_and_ranges_include_the_upper_bound():
    runs = upcoming("*/20 9-10 * * *", datetime(2025, 3, 3, 8, 0), 6)
    assert [(r.hour, r.minute) for r in runs] == [(9, 0), (9, 20), (9, 40), (10, 0), (10, 20), (10, 40)]
    spec = CronSpec("0 8-18/5 * * *")
    assert spec.hours == {8, 13, 18}, "8-18/5 is 8, 13, 18: the end of a range is inclusive"
    assert CronSpec("5/20 * * * *").minutes == {5, 25, 45}


def test_weekday_numbers_follow_cron_convention():
    # 2025-03-03 is a Monday. In cron: 0 or 7 = Sunday, 1 = Monday.
    assert nxt("0 6 * * 1", datetime(2025, 3, 2, 12, 0)) == datetime(2025, 3, 3, 6, 0)
    assert nxt("0 6 * * 0", datetime(2025, 3, 3, 12, 0)) == datetime(2025, 3, 9, 6, 0)
    assert nxt("0 6 * * 7", datetime(2025, 3, 3, 12, 0)) == datetime(2025, 3, 9, 6, 0)
    assert nxt("0 6 * * 1-5", datetime(2025, 3, 7, 12, 0)) == datetime(2025, 3, 10, 6, 0)


def test_day_of_month_and_weekday_are_or_when_both_restricted():
    # "the 13th, or any Friday". 2025-06-13 is a Friday; 2025-06-06 is also a Friday.
    runs = upcoming("0 0 13 * 5", datetime(2025, 6, 1, 0, 0), 4)
    assert runs == [datetime(2025, 6, 6), datetime(2025, 6, 13), datetime(2025, 6, 20), datetime(2025, 6, 27)]


def test_one_restricted_day_field_behaves_as_and_with_star():
    assert nxt("0 0 15 * *", datetime(2025, 1, 16, 0, 0)) == datetime(2025, 2, 15)
    assert nxt("0 0 * * 6", datetime(2025, 3, 3, 0, 0)) == datetime(2025, 3, 8)


def test_rolls_over_months_years_and_leap_days():
    assert nxt("0 0 1 1 *", datetime(2025, 6, 1, 0, 0)) == datetime(2026, 1, 1)
    assert nxt("59 23 31 * *", datetime(2025, 4, 30, 23, 59)) == datetime(2025, 5, 31, 23, 59)
    assert nxt("0 0 29 2 *", datetime(2025, 3, 1, 0, 0)) == datetime(2028, 2, 29)
    assert nxt("15 4 * * *", datetime(2025, 12, 31, 23, 59)) == datetime(2026, 1, 1, 4, 15)


def test_invalid_expressions_are_rejected():
    for bad in ("* * * *", "61 * * * *", "* 24 * * *", "* * 0 * *", "*/0 * * * *", "10-5 * * * *"):
        with pytest.raises(ValueError):
            CronSpec(bad)
    with pytest.raises(ValueError):
        nxt("0 0 31 2 *", datetime(2025, 1, 1))
