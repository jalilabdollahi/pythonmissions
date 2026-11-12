import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import read_state, failed_units, active_units, summary


def fake_runner(states):
    def runner(argv):
        unit = argv[-1]
        return (states[unit] + "\n").encode("utf-8")
    return runner


STATES = {"nginx.service": "active", "db.service": "failed", "cron.service": "Active"}


def test_read_state_returns_text_not_bytes():
    state = read_state(fake_runner(STATES), "nginx.service")
    assert isinstance(state, str), "decode the bytes the runner returns"
    assert state == "active"


def test_read_state_normalises_case():
    assert read_state(fake_runner(STATES), "cron.service") == "active"


def test_only_failed_units_are_reported():
    assert failed_units(fake_runner(STATES), list(STATES)) == ["db.service"]


def test_active_units_parses_listing_bytes():
    raw = b"nginx.service loaded active running\ndb.service loaded failed failed\n\ncron.service loaded active running\n"
    assert active_units(raw) == ["nginx.service", "cron.service"]


def test_summary_messages():
    assert summary(fake_runner(STATES), ["nginx.service"]) == "all units active"
    assert summary(fake_runner(STATES), ["nginx.service", "db.service"]) == "failed: db.service"
