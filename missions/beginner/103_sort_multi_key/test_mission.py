import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import sort_incidents, top_names, count_by_priority

INCIDENTS = [
    {"name": "checkout", "priority": 3},
    {"name": "auth", "priority": 3},
    {"name": "Billing", "priority": 3},
    {"name": "reports", "priority": 1},
    {"name": "search", "priority": 2},
    {"name": "audit", "priority": 1},
]


def test_highest_priority_comes_first():
    ordered = sort_incidents(INCIDENTS)
    assert [i["priority"] for i in ordered] == [3, 3, 3, 2, 1, 1]


def test_names_ascend_within_the_same_priority():
    names = [i["name"] for i in sort_incidents(INCIDENTS) if i["priority"] == 3]
    assert names == ["auth", "Billing", "checkout"], "ties on priority are broken A to Z, ignoring case"


def test_low_priority_group_is_alphabetical_too():
    names = [i["name"] for i in sort_incidents(INCIDENTS) if i["priority"] == 1]
    assert names == ["audit", "reports"]


def test_input_is_not_modified():
    before = list(INCIDENTS)
    sort_incidents(INCIDENTS)
    assert INCIDENTS == before


def test_top_names_respects_limit():
    assert top_names(INCIDENTS, 2) == ["auth", "Billing"]


def test_count_by_priority():
    assert count_by_priority(INCIDENTS) == {3: 3, 1: 2, 2: 1}
