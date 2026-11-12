import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import failover_order, first_standby, describe


def test_returns_sorted_hosts():
    assert failover_order(["c", "a", "b"]) == ["a", "b", "c"], "sort() returns None; use sorted()"


def test_input_list_is_left_alone():
    hosts = ["c", "a", "b"]
    failover_order(hosts)
    assert hosts == ["c", "a", "b"]


def test_empty_list():
    assert failover_order([]) == []


def test_first_standby():
    assert first_standby(["standby-b", "standby-a"]) == "standby-a"
    assert first_standby([]) is None


def test_describe_text():
    assert describe(["b", "c", "a"]) == "try: a -> b -> c"
    assert describe([]) == "no standbys"
