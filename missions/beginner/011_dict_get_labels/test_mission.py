import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import team_of, count_by_team, unowned_pods

PODS = [
    {"name": "cart-1", "labels": {"team": "checkout", "tier": "web"}},
    {"name": "cart-2", "labels": {"team": "checkout"}},
    {"name": "search-1", "labels": {"team": "discovery"}},
    {"name": "scratch-7", "labels": {}},
    {"name": "tmp-9", "labels": {"tier": "batch"}},
]


def test_labeled_pod_returns_its_team():
    assert team_of(PODS[0]) == "checkout"


def test_missing_team_is_unowned():
    assert team_of(PODS[3]) == "unowned", "an unlabeled pod must not crash the report"


def test_other_labels_do_not_count_as_team():
    assert team_of(PODS[4]) == "unowned"


def test_count_by_team_includes_unowned():
    assert count_by_team(PODS) == {"checkout": 2, "discovery": 1, "unowned": 2}


def test_unowned_pod_names():
    assert unowned_pods(PODS) == ["scratch-7", "tmp-9"]


def test_empty_cluster():
    assert count_by_team([]) == {}
