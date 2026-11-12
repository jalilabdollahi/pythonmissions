import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import parse_version, is_newer, latest_release, needs_upgrade, hosts_to_upgrade


def test_parse_version_gives_ints():
    assert parse_version("1.10.0") == (1, 10, 0)


def test_minor_ten_is_newer_than_minor_nine():
    assert is_newer("1.10.0", "1.9.0") is True, "compare numbers, not characters"


def test_older_is_not_newer_and_equal_is_not_newer():
    assert is_newer("1.2.3", "1.10.0") is False
    assert is_newer("2.0.0", "2.0.0") is False


def test_major_version_dominates():
    assert is_newer("10.0.0", "9.99.99") is True


def test_latest_release_picks_numerically_highest():
    assert latest_release(["1.9.0", "1.10.0", "1.2.7", "1.10.0"]) == "1.10.0"


def test_needs_upgrade():
    assert needs_upgrade("1.9.0", "1.10.0") is True
    assert needs_upgrade("1.10.0", "1.9.0") is False


def test_hosts_to_upgrade():
    fleet = {"web-1": "1.9.0", "web-2": "1.10.0", "db-1": "1.2.3"}
    assert hosts_to_upgrade(fleet, "1.10.0") == ["db-1", "web-1"]
