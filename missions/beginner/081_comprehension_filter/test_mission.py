import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import running_names, stopped_names, removable, cleanup_plan, describe

FLEET = [
    {"name": "web", "state": "running", "age_hours": 72},
    {"name": "job-41", "state": "exited", "age_hours": 30},
    {"name": "job-42", "state": "created", "age_hours": 1},
    {"name": "job-43", "state": "dead", "age_hours": 48},
]


def test_running_names_lists_only_live_containers():
    assert running_names(FLEET) == ["web"]


def test_stopped_names_lists_every_non_running_container():
    assert stopped_names(FLEET) == ["job-41", "job-42", "job-43"], "the comprehension filter is inverted"


def test_removable_needs_stopped_and_old_enough():
    assert removable(FLEET, 24) == ["job-41", "job-43"]


def test_removable_never_includes_running_containers():
    assert "web" not in removable(FLEET, 0)


def test_age_exactly_at_limit_is_removable():
    assert removable([{"name": "x", "state": "exited", "age_hours": 24}], 24) == ["x"]


def test_cleanup_plan_commands():
    assert cleanup_plan(FLEET, 24) == ["docker rm job-41", "docker rm job-43"]


def test_describe_counts():
    assert describe(FLEET) == "1 running, 3 stopped"
    assert describe([]) == "0 running, 0 stopped"
