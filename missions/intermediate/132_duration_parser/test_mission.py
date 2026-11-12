import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import broken


def test_seconds_minutes_hours():
    assert broken.parse_duration("15s") == 15
    assert broken.parse_duration("2m") == 120
    assert broken.parse_duration("1h") == 3600, "an hour is 3600 seconds"


def test_compound_duration():
    assert broken.parse_duration("1h30m15s") == 5415


def test_days_and_weeks():
    assert broken.parse_duration("2d") == 172800
    assert broken.parse_duration("1w") == 604800
    assert broken.parse_duration("1w2d") == 604800 + 172800


def test_plain_number_is_seconds():
    assert broken.parse_duration("45") == 45


def test_units_may_be_in_any_order():
    assert broken.parse_duration("30m1h") == 5400


def test_garbage_is_rejected_not_ignored():
    for bad in ("10 minutes", "1h xyz", "", "h", "5x", "1h30"):
        with pytest.raises(ValueError):
            broken.parse_duration(bad)


def test_format_duration_round_trip():
    assert broken.format_duration(5415) == "1h30m15s"
    assert broken.format_duration(0) == "0s"
    assert broken.format_duration(691200) == "1w1d"
    assert broken.parse_duration(broken.format_duration(98765)) == 98765
