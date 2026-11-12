import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import Router, status_line, freshly_rebooted


def test_uptime_seconds_reads_like_an_attribute():
    assert Router("a", 1000, 4600).uptime_seconds == 3600


def test_uptime_hours_is_a_number():
    r = Router("a", 0, 9000)
    assert r.uptime_hours == 2.5, "decorate the method with @property"


def test_uptime_follows_changes_to_now():
    r = Router("a", 0, 3600)
    r.now = 7200
    assert r.uptime_hours == 2.0


def test_is_fresh_for_recent_boot():
    assert Router("a", 1000, 1500).is_fresh is True


def test_is_not_fresh_after_an_hour():
    assert Router("a", 0, 3600).is_fresh is False


def test_status_line():
    assert status_line(Router("edge-1", 0, 9000)) == "edge-1 up 2.5h"


def test_freshly_rebooted_lists_names():
    fleet = [Router("old", 0, 90000), Router("new", 89000, 90000)]
    assert freshly_rebooted(fleet) == ["new"]
