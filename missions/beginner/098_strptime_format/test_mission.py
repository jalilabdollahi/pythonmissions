import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import parse_app_ts, parse_access_ts, outage_minutes, same_hour


def test_app_timestamp_fields_land_in_the_right_place():
    assert parse_app_ts("2024-03-05 14:07:09") == datetime(2024, 3, 5, 14, 7, 9), "%m is month, %M is minute"


def test_app_timestamp_with_large_minutes():
    assert parse_app_ts("2024-11-30 09:59:58") == datetime(2024, 11, 30, 9, 59, 58)


def test_access_timestamp_afternoon_hour():
    assert parse_access_ts("05/Mar/2024:14:07:09") == datetime(2024, 3, 5, 14, 7, 9), "%H is the 24-hour clock"


def test_access_timestamp_morning_and_midnight():
    assert parse_access_ts("01/Jan/2025:00:00:00") == datetime(2025, 1, 1, 0, 0, 0)
    assert parse_access_ts("31/Dec/2024:23:59:59").hour == 23


def test_both_formats_agree_on_the_same_moment():
    assert parse_app_ts("2024-03-05 14:07:09") == parse_access_ts("05/Mar/2024:14:07:09")


def test_outage_minutes_crosses_the_hour():
    assert outage_minutes("2024-03-05 14:07:09", "2024-03-05 15:30:09") == 83


def test_same_hour():
    assert same_hour(datetime(2024, 3, 5, 14, 1), datetime(2024, 3, 5, 14, 59))
    assert not same_hour(datetime(2024, 3, 5, 14, 1), datetime(2024, 3, 6, 14, 1))
