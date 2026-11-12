import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

from broken import (
    PERIOD_HOURS,
    burn_rate,
    error_ratio,
    evaluate,
    hours_to_exhaustion,
    steady_traffic,
    top_severity,
    window_counts,
)

NOW = 90000


def test_error_ratio_is_errors_over_total_requests():
    buckets = [(100, 100, 10)]
    assert error_ratio(buckets, 100, 60) == pytest.approx(0.10), "total already includes the failures"


def test_empty_window_has_zero_errors_not_total_failure():
    assert error_ratio([], NOW, 300) == 0.0
    assert evaluate([], NOW) == []


def test_burn_rate_is_relative_to_the_error_budget():
    assert burn_rate(0.001) == pytest.approx(1.0)
    assert burn_rate(0.0144) == pytest.approx(14.4)
    assert burn_rate(0.0) == 0.0


def test_window_is_half_open_on_the_old_side():
    buckets = [(940, 10, 1), (941, 10, 1), (1000, 10, 1)]
    assert window_counts(buckets, now=1000, seconds=60) == (20, 2)


def test_brief_spike_alone_does_not_page():
    traffic = steady_traffic(NOW - 7200, NOW, 1000, lambda ts: 0.05 if ts > NOW - 240 else 0.0)
    assert top_severity(evaluate(traffic, NOW)) != "page", "short window is hot but the 1h/6h windows barely moved"


def test_old_incident_that_has_recovered_does_not_page():
    traffic = steady_traffic(NOW - 7200, NOW, 1000, lambda ts: 0.05 if ts < NOW - 3000 else 0.0)
    assert top_severity(evaluate(traffic, NOW)) != "page", "long window is hot but the short window shows recovery"


def test_sustained_outage_pages_on_both_windows():
    traffic = steady_traffic(NOW - 21600, NOW, 1000, lambda ts: 0.02)
    alerts = evaluate(traffic, NOW)
    assert top_severity(alerts) == "page"
    assert {a["window"] for a in alerts} >= {3600, 21600}
    assert all(a["burn"] == pytest.approx(20.0) for a in alerts)


def test_slow_leak_creates_a_ticket_not_a_page():
    traffic = steady_traffic(NOW - 259200, NOW, 1000, lambda ts: 0.002)
    alerts = evaluate(traffic, NOW)
    assert [a["severity"] for a in alerts] == ["ticket"]
    assert top_severity([]) == "ok"


def test_hours_to_exhaustion():
    assert hours_to_exhaustion(1.0) == PERIOD_HOURS
    assert hours_to_exhaustion(14.4) == pytest.approx(50.0)
    assert hours_to_exhaustion(0) is None
