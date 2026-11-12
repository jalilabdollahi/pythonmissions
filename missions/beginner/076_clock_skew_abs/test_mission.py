import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import skew_seconds, is_skewed, find_skewed_hosts, worst_offender, format_report

REF = 1_700_000_000


def test_skew_is_host_minus_reference():
    assert skew_seconds(REF - 40, REF) == -40


def test_clock_running_ahead_is_flagged():
    assert is_skewed(REF + 120, REF, 30)


def test_clock_running_behind_is_flagged_too():
    assert is_skewed(REF - 300, REF, 30), "negative drift must count: compare the magnitude"


def test_small_drift_either_way_is_fine():
    assert not is_skewed(REF + 10, REF, 30)
    assert not is_skewed(REF - 10, REF, 30)


def test_exactly_at_tolerance_is_allowed():
    assert not is_skewed(REF - 30, REF, 30)


def test_find_skewed_hosts_returns_sorted_names():
    readings = {"db-3": REF + 90, "db-1": REF, "db-2": REF - 300}
    assert find_skewed_hosts(readings, REF, 30) == ["db-2", "db-3"]


def test_worst_offender_uses_magnitude():
    readings = {"a": REF + 50, "b": REF - 400, "c": REF + 5}
    assert worst_offender(readings, REF) == "b"


def test_report_shows_signed_drift():
    readings = {"db-2": REF - 300, "db-1": REF}
    assert format_report(readings, REF, 30) == "db-2: -300s"
    assert format_report({"x": REF}, REF, 30) == "all clocks in sync"
