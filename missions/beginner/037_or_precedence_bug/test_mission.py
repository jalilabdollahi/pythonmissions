import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import healthy_services, is_acceptable, status_banner

STATUSES = {"api": "ok", "ledger": "critical", "search": "warn", "cache": "unknown"}


def test_ok_is_acceptable():
    assert is_acceptable("ok") is True


def test_warn_is_acceptable():
    assert is_acceptable("warn") is True


def test_critical_is_not_acceptable():
    assert is_acceptable("critical") is False, "critical must never pass as healthy"


def test_unknown_state_is_not_acceptable():
    assert is_acceptable("unknown") is False
    assert is_acceptable("") is False


def test_healthy_services_filters_bad_ones():
    assert healthy_services(STATUSES) == ["api", "search"]


def test_banner_reports_degraded_count():
    assert status_banner(STATUSES) == "2 service(s) degraded"
    assert status_banner({"api": "ok"}) == "All systems operational"
