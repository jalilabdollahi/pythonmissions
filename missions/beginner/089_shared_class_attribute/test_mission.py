import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import Server, least_loaded, dispatch


def test_new_server_has_empty_queue():
    assert Server("a", 2).jobs == []


def test_assign_adds_job_when_room():
    s = Server("a", 2)
    assert s.assign("etl") is True
    assert s.load() == 1


def test_queues_are_independent_between_servers():
    a, b = Server("a", 5), Server("b", 5)
    a.assign("etl")
    a.assign("report")
    assert b.load() == 0, "each instance needs its own list created in __init__"
    assert b.jobs == []


def test_full_server_rejects_jobs():
    s = Server("a", 1)
    assert s.assign("one")
    assert s.assign("two") is False
    assert not s.has_room()


def test_capacity_is_per_server():
    a, b = Server("a", 1), Server("b", 3)
    a.assign("x")
    assert b.has_room()
    assert b.assign("y") is True


def test_least_loaded_picks_emptiest():
    a, b = Server("a", 5), Server("b", 5)
    a.assign("x")
    assert least_loaded([a, b]) is b


def test_dispatch_spreads_jobs():
    pool = [Server("node-a", 2), Server("node-b", 2)]
    placed = dispatch(pool, ["etl", "report", "export"])
    assert placed == {"etl": "node-a", "report": "node-b", "export": "node-a"}
