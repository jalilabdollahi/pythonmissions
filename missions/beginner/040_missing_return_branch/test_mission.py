import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import datetime

import pytest

from broken import expiry_date, retention_days


def test_hot_retention():
    assert retention_days("hot") == 7


def test_warm_retention():
    assert retention_days("warm") == 30


def test_cold_retention_returns_a_number():
    assert retention_days("cold") == 365, "every tier must return its number of days"


def test_unknown_tier_is_rejected():
    with pytest.raises(ValueError):
        retention_days("lukewarm")


def test_expiry_date_for_cold_backup():
    created = datetime.date(2024, 1, 1)
    assert expiry_date("cold", created) == datetime.date(2024, 12, 31)


def test_expiry_date_for_hot_backup():
    assert expiry_date("hot", datetime.date(2024, 3, 1)) == datetime.date(2024, 3, 8)
