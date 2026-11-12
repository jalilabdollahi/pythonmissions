import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import broken


def fake_fetch(table, seen=None):
    def fetch(url, timeout):
        if seen is not None:
            seen.append((url, timeout))
        outcome = table[url]
        if isinstance(outcome, BaseException):
            raise outcome
        return outcome
    return fetch


def check(name, url, **extra):
    return dict(name=name, url=url, **extra)


def test_2xx_is_up_and_5xx_is_down():
    fetch = fake_fetch({"u1": 200, "u2": 204, "u3": 503})
    states = [r["state"] for r in broken.run_all([check("a", "u1"), check("b", "u2"), check("c", "u3")], fetch)]
    assert states == ["up", "up", "down"]


def test_redirects_and_client_errors_are_degraded_not_up():
    fetch = fake_fetch({"u1": 302, "u2": 404, "u3": 301})
    states = [broken.run_check(check("x", u), fetch)["state"] for u in ("u1", "u2", "u3")]
    assert states == ["degraded"] * 3, "a 302 to a login page is not a healthy service"


def test_timeout_is_reported_as_timeout():
    fetch = fake_fetch({"u": TimeoutError("slow")})
    assert broken.run_check(check("api", "u"), fetch) == {"name": "api", "state": "timeout"}


def test_other_os_errors_are_unreachable():
    fetch = fake_fetch({"u": ConnectionRefusedError("no"), "v": OSError("route")})
    assert broken.run_check(check("a", "u"), fetch)["state"] == "unreachable"
    assert broken.run_check(check("b", "v"), fetch)["state"] == "unreachable"


def test_per_check_timeout_is_passed_to_fetch():
    seen = []
    fetch = fake_fetch({"fast": 200, "batch": 200}, seen)
    broken.run_all([check("f", "fast"), check("b", "batch", timeout=10)], fetch)
    assert seen == [("fast", 2.0), ("batch", 10)]


def test_run_all_keeps_order():
    fetch = fake_fetch({"1": 200, "2": 500})
    assert [r["name"] for r in broken.run_all([check("two", "2"), check("one", "1")], fetch)] == ["two", "one"]


def test_overall_rollup():
    up = {"name": "a", "state": "up"}
    assert broken.overall([up, up]) == "ok"
    assert broken.overall([]) == "ok"
    assert broken.overall([up, {"name": "b", "state": "degraded"}]) == "warning"
    assert broken.overall([up, {"name": "b", "state": "timeout"}]) == "critical"
    assert broken.overall([{"name": "b", "state": "degraded"}, {"name": "c", "state": "down"}]) == "critical"
