import os
import sys
from datetime import datetime, timedelta, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import utc_now, parse_expiry, is_expired, expired_ids, seconds_to_expiry

NOW = datetime(2025, 6, 1, 8, 30, 0, tzinfo=timezone.utc)


def test_utc_now_is_timezone_aware():
    now = utc_now()
    assert now.tzinfo is not None, "naive datetimes cannot be compared with aware ones"
    assert now.utcoffset() == timedelta(0)


def test_parse_expiry_is_aware_utc():
    parsed = parse_expiry("2025-06-01T08:30:00")
    assert parsed.tzinfo is not None
    assert parsed == NOW


def test_token_at_exact_expiry_is_expired():
    assert is_expired({"id": "a", "expires": "2025-06-01T08:30:00"}, NOW)


def test_future_token_is_not_expired():
    assert not is_expired({"id": "a", "expires": "2025-06-01T08:30:01"}, NOW)


def test_past_token_is_expired():
    assert is_expired({"id": "a", "expires": "2024-12-31T23:59:59"}, NOW)


def test_expired_ids_sorted():
    tokens = [
        {"id": "z", "expires": "2025-01-01T00:00:00"},
        {"id": "m", "expires": "2026-01-01T00:00:00"},
        {"id": "b", "expires": "2025-05-01T00:00:00"},
    ]
    assert expired_ids(tokens, NOW) == ["b", "z"]


def test_seconds_to_expiry():
    assert seconds_to_expiry({"id": "a", "expires": "2025-06-01T08:31:00"}, NOW) == 60
