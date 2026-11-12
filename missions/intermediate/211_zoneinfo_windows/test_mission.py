import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime, timezone

import broken


def utc(*args):
    return datetime(*args, tzinfo=timezone.utc)


def test_winter_berlin_is_utc_plus_one():
    start, end = broken.window_to_utc("2024-01-15", "22:00", 60, "Europe/Berlin")
    assert start == utc(2024, 1, 15, 21, 0)
    assert end == utc(2024, 1, 15, 22, 0)


def test_summer_berlin_is_utc_plus_two():
    start, _ = broken.window_to_utc("2024-07-15", "22:00", 60, "Europe/Berlin")
    assert start == utc(2024, 7, 15, 20, 0), "a fixed +1 offset is wrong in summer"


def test_new_york_summer_is_utc_minus_four():
    start, _ = broken.window_to_utc("2024-07-01", "02:00", 90, "America/New_York")
    assert start == utc(2024, 7, 1, 6, 0)


def test_duration_is_real_elapsed_time_across_spring_forward():
    start, end = broken.window_to_utc("2024-03-31", "00:30", 240, "Europe/Berlin")
    assert start == utc(2024, 3, 30, 23, 30)
    assert end == utc(2024, 3, 31, 3, 30), "4 hours of real time, even though a local hour was skipped"


def test_duration_is_real_elapsed_time_across_fall_back():
    start, end = broken.window_to_utc("2024-11-03", "00:30", 180, "America/New_York")
    assert start == utc(2024, 11, 3, 4, 30)
    assert end == utc(2024, 11, 3, 7, 30)


def test_local_label_converts_instead_of_relabeling():
    assert broken.local_label(utc(2024, 7, 15, 20, 0), "Europe/Berlin") == "2024-07-15 22:00 CEST"
    assert broken.local_label(utc(2024, 1, 15, 21, 0), "Europe/Berlin") == "2024-01-15 22:00 CET"


def test_announce_across_the_clock_change():
    assert broken.announce("2024-03-31", "00:30", 240, "Europe/Berlin") == "2024-03-31 00:30 CET -> 2024-03-31 05:30 CEST"


def test_daily_windows_follow_the_zone_rules():
    windows = broken.daily_windows("2024-03-30", "22:00", 60, "Europe/Berlin", 3)
    assert [to_iso(w[0]) for w in windows] == ["2024-03-30T21:00:00Z", "2024-03-31T20:00:00Z", "2024-04-01T20:00:00Z"]


def to_iso(dt):
    return broken.to_iso_z(dt)


def test_overlap_detection():
    a = broken.window_to_utc("2024-07-15", "22:00", 60, "Europe/Berlin")
    b = broken.window_to_utc("2024-07-15", "22:30", 60, "Europe/Berlin")
    c = broken.window_to_utc("2024-07-15", "23:00", 60, "Europe/Berlin")
    assert broken.windows_overlap(a, b)
    assert not broken.windows_overlap(a, c)
