import copy
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import broken


def inc(id_, severity, opened, team="core"):
    return {"id": id_, "severity": severity, "opened": opened, "team": team}


def make_queue():
    return [
        inc("INC-5", "low", "2024-05-01T07:00"),
        inc("INC-4", "high", "2024-05-01T09:00"),
        inc("INC-3", "critical", "2024-05-01T10:30"),
        inc("INC-2", "high", "2024-05-01T08:00"),
        inc("INC-1", "medium", "2024-05-01T06:00"),
        inc("INC-6", "high", "2024-05-01T08:00"),
    ]


def ids(items):
    return [i["id"] for i in items]


def test_severity_is_the_primary_key():
    result = broken.triage_order(make_queue())
    assert ids(result)[0] == "INC-3", "critical outranks everything, even when opened later"


def test_same_severity_is_ordered_by_opened_time():
    result = broken.triage_order(make_queue())
    assert ids(result)[1:4] == ["INC-2", "INC-6", "INC-4"]


def test_equal_severity_and_time_fall_back_to_id():
    result = broken.triage_order(make_queue())
    assert ids(result).index("INC-2") < ids(result).index("INC-6")


def test_medium_ranks_above_low_not_alphabetically_below():
    result = broken.triage_order(make_queue())
    assert ids(result)[-2:] == ["INC-1", "INC-5"]


def test_input_list_is_not_modified():
    queue = make_queue()
    original = copy.deepcopy(queue)
    broken.triage_order(queue)
    assert queue == original, "use sorted() so callers keep their own order"


def test_page_list_and_team_grouping():
    assert broken.oncall_page_list(make_queue(), limit=2) == ["INC-3", "INC-2"]
    queue = [inc("A", "low", "t1", "db"), inc("B", "high", "t2", "db"), inc("C", "high", "t0", "web")]
    assert broken.group_by_team(queue) == {"web": ["C"], "db": ["B", "A"]}


def test_severity_counts_in_rank_order():
    counts = broken.severity_counts(make_queue())
    assert list(counts) == ["critical", "high", "medium", "low"]
    assert counts["high"] == 3
