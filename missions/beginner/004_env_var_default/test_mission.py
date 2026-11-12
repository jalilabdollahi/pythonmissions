import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

from broken import load_settings, describe


def test_only_region_is_enough():
    assert load_settings({"REGION": "eu-west"})["region"] == "eu-west"


def test_retention_defaults_to_seven_days():
    assert load_settings({"REGION": "eu-west"})["retention_days"] == "7"


def test_notify_email_defaults_to_empty():
    assert load_settings({"REGION": "eu-west"})["notify_email"] == ""


def test_explicit_values_win_over_defaults():
    s = load_settings({"REGION": "us-1", "RETENTION_DAYS": "30", "NOTIFY_EMAIL": "ops@example.com"})
    assert s["retention_days"] == "30"
    assert s["notify_email"] == "ops@example.com"


def test_missing_region_still_fails_loudly():
    with pytest.raises(KeyError):
        load_settings({"RETENTION_DAYS": "3"})


def test_describe_skips_empty_email():
    assert describe(load_settings({"REGION": "eu-west"})) == "region=eu-west, retention=7d"
