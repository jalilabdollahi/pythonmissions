import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import broken

ROUTES = [
    {"match": {"team": "payments", "severity": "page"}, "receiver": "payments-pager"},
    {"match": {"team": "payments"}, "receiver": "payments-slack"},
    {"match": {"service": "cdn"}, "receiver": "edge-oncall"},
    {"match": {}, "receiver": "catch-all"},
]


def test_most_specific_first_route_wins():
    labels = {"team": "payments", "severity": "page"}
    assert broken.pick_receiver(labels, ROUTES, "fallback") == "payments-pager", "first matching route wins"


def test_later_route_used_when_first_does_not_match():
    labels = {"team": "payments", "severity": "ticket"}
    assert broken.pick_receiver(labels, ROUTES, "fallback") == "payments-slack"


def test_all_matchers_must_match():
    labels = {"team": "payments", "service": "db"}
    routes = [{"match": {"team": "payments", "severity": "page"}, "receiver": "pager"}]
    assert broken.pick_receiver(labels, routes, "fallback") == "fallback", "severity is missing so the route must not match"


def test_missing_label_does_not_match():
    routes = [{"match": {"env": "prod"}, "receiver": "prod-team"}]
    assert broken.pick_receiver({"service": "x"}, routes, "nobody") == "nobody"


def test_default_receiver_when_nothing_matches():
    routes = [{"match": {"service": "cdn"}, "receiver": "edge-oncall"}]
    assert broken.pick_receiver({"service": "db"}, routes, "triage") == "triage"


def test_empty_match_matches_everything():
    assert broken.pick_receiver({"a": "b"}, [{"match": {}, "receiver": "all"}], "d") == "all"


def test_route_alerts_groups_names_by_receiver():
    alerts = [
        {"name": "PayFail", "labels": {"team": "payments", "severity": "page"}},
        {"name": "PayLag", "labels": {"team": "payments", "severity": "info"}},
        {"name": "EdgeDown", "labels": {"service": "cdn"}},
        {"name": "PayFail2", "labels": {"team": "payments", "severity": "page"}},
    ]
    assert broken.route_alerts(alerts, ROUTES[:3], "triage") == {
        "payments-pager": ["PayFail", "PayFail2"],
        "payments-slack": ["PayLag"],
        "edge-oncall": ["EdgeDown"],
    }
