import os
import sys
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import days_left, hours_left, expiring_soon, report, most_urgent

NOW = datetime(2025, 1, 1, 12, 0, 0)


def test_days_left_for_far_expiry():
    assert days_left(NOW + timedelta(days=40, hours=3), NOW) == 40, ".seconds only holds the part below one day"


def test_days_left_under_one_day_is_zero():
    assert days_left(NOW + timedelta(hours=10), NOW) == 0


def test_days_left_negative_when_expired():
    assert days_left(NOW - timedelta(days=2), NOW) == -2


def test_hours_left_counts_whole_duration():
    assert hours_left(NOW + timedelta(days=2, hours=6), NOW) == 54.0


def test_hours_left_negative_when_expired():
    assert hours_left(NOW - timedelta(hours=5), NOW) == -5.0


def test_expiring_soon_is_sorted_and_inclusive():
    certs = {
        "b.example.com": NOW + timedelta(days=30, hours=1),
        "a.example.com": NOW + timedelta(days=5),
        "c.example.com": NOW + timedelta(days=90),
    }
    assert expiring_soon(certs, NOW, 30) == ["a.example.com", "b.example.com"]


def test_report_lines():
    certs = {"shop.example.com": NOW + timedelta(days=12, hours=3)}
    assert report(certs, NOW, 30) == ["shop.example.com: 12 days"]


def test_most_urgent():
    certs = {"x": NOW + timedelta(days=9), "y": NOW + timedelta(days=2)}
    assert most_urgent(certs, NOW) == "y"
    assert most_urgent({}, NOW) is None
