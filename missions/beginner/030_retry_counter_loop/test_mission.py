import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

from broken import call_with_retries, export_invoices


class FlakyAction:
    """Fails `failures` times, then succeeds. Aborts the test if called too often."""

    def __init__(self, failures):
        self.failures = failures
        self.calls = 0

    def __call__(self):
        self.calls += 1
        assert self.calls <= 25, "action called far too many times: the retry loop never ends"
        if self.calls <= self.failures:
            raise ConnectionError("ledger unreachable")
        return "ok"


def test_success_on_first_try_returns_value():
    action = FlakyAction(0)
    assert call_with_retries(action) == "ok"
    assert action.calls == 1


def test_recovers_after_transient_failures():
    action = FlakyAction(2)
    assert call_with_retries(action, max_attempts=3) == "ok"
    assert action.calls == 3


def test_gives_up_after_max_attempts():
    action = FlakyAction(100)
    with pytest.raises(RuntimeError, match="4 attempts"):
        call_with_retries(action, max_attempts=4)
    assert action.calls == 4, "must stop exactly at max_attempts"


def test_delay_doubles_between_attempts():
    delays = []
    with pytest.raises(RuntimeError):
        call_with_retries(FlakyAction(100), max_attempts=4, sleep=delays.append)
    assert delays[:3] == [1, 2, 4]


def test_export_collects_every_page():
    assert export_invoices(lambda p: f"page-{p}", 3) == ["page-0", "page-1", "page-2"]
