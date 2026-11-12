import os
import sys
import time

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import broken

# 2024-05-01T12:00:00Z
EPOCH = 1714564800


@pytest.fixture(autouse=True)
def boston_clock(monkeypatch):
    """Run every test as if the machine were set to America/New_York."""
    if not hasattr(time, "tzset"):
        yield
        return
    monkeypatch.setenv("TZ", "America/New_York")
    time.tzset()
    yield
    monkeypatch.undo()
    time.tzset()


def test_epoch_to_iso_is_utc_whatever_the_machine_zone():
    assert broken.epoch_to_iso(EPOCH) == "2024-05-01T12:00:00Z"


def test_epoch_zero():
    assert broken.epoch_to_iso(0) == "1970-01-01T00:00:00Z"


def test_milliseconds_are_divided_and_preserved():
    assert broken.epoch_ms_to_iso(EPOCH * 1000 + 123) == "2024-05-01T12:00:00.123Z"


def test_z_suffix_means_utc():
    assert broken.iso_to_epoch("2024-05-01T12:00:00Z") == EPOCH


def test_explicit_offsets_are_honoured():
    assert broken.iso_to_epoch("2024-05-01T14:00:00+02:00") == EPOCH
    assert broken.iso_to_epoch("2024-05-01T07:00:00-05:00") == EPOCH


def test_roundtrip():
    assert broken.iso_to_epoch(broken.epoch_to_iso(EPOCH + 86400)) == EPOCH + 86400


def test_hour_bucket_and_age_label():
    assert broken.hour_bucket(EPOCH + 1234) == "2024-05-01T12:00:00Z"
    assert broken.age_label(EPOCH + 45, "2024-05-01T12:00:00Z") == "45s ago"
    assert broken.age_label(EPOCH + 600, "2024-05-01T12:00:00Z") == "10m ago"
    assert broken.age_label(EPOCH + 7300, "2024-05-01T14:00:00+02:00") == "2h ago"


def test_seconds_between_and_stamp():
    assert broken.seconds_between("2024-05-01T12:00:00Z", "2024-05-01T12:05:30Z") == 330
    assert broken.ticket_stamp(EPOCH) == "[2024-05-01T12:00:00Z]"
