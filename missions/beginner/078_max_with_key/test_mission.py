import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import most_free_node, least_free_node, pick_for_job, summary

NODES = {"worker-1": 2048, "worker-2": 512, "worker-9": 128}


def test_most_free_node_is_chosen_by_value_not_name():
    assert most_free_node(NODES) == "worker-1", "max over a dict compares keys unless you pass key="


def test_most_free_node_when_value_leader_is_alphabetically_first():
    assert most_free_node({"a": 900, "z": 10}) == "a"


def test_least_free_node_is_chosen_by_value():
    assert least_free_node(NODES) == "worker-9"
    assert least_free_node({"a": 1, "z": 99}) == "a"


def test_empty_cluster_returns_none():
    assert most_free_node({}) is None
    assert least_free_node({}) is None


def test_pick_for_job_returns_node_with_enough_room():
    assert pick_for_job(NODES, 1024) == "worker-1"


def test_pick_for_job_returns_none_when_nothing_fits():
    assert pick_for_job(NODES, 4096) is None


def test_summary_reads_correctly():
    assert summary(NODES) == "most free: worker-1 (2048 MB), least free: worker-9 (128 MB)"
    assert summary({}) == "no nodes"
