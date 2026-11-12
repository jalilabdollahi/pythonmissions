import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

from broken import LeastConnections, NoCapacity, route_many


def test_connections_spread_by_load_per_weight():
    lb = LeastConnections({"big": 3, "small": 1})
    assert route_many(lb, 5) == ["big", "small", "big", "big", "small"]
    assert lb.snapshot() == {"big": 3, "small": 2}
    assert lb.utilization() == {"big": 1.0, "small": 2.0}


def test_idle_servers_are_rotated_instead_of_always_picking_the_first():
    lb = LeastConnections({"a": 1, "b": 1, "c": 1})
    picks = []
    for _ in range(6):
        lease = lb.acquire()
        picks.append(lease.server)
        lb.release(lease)
    assert picks == ["a", "b", "c", "a", "b", "c"], "equal load must be broken by least recently used"


def test_release_returns_capacity_to_the_server_it_came_from():
    lb = LeastConnections({"a": 1, "b": 1})
    first = lb.acquire()
    second = lb.acquire()
    assert (first.server, second.server) == ("a", "b")
    assert lb.release(first) is True
    assert lb.snapshot() == {"a": 0, "b": 1}
    assert lb.acquire().server == "a"


def test_releasing_a_lease_twice_only_counts_once():
    lb = LeastConnections({"a": 1, "b": 1})
    first = lb.acquire()
    lb.acquire()
    assert lb.release(first) is True
    assert lb.release(first) is False
    assert lb.snapshot() == {"a": 0, "b": 1}, "a retried release must not make the load negative"
    assert lb.acquire().server == "a"


def test_draining_server_gets_no_new_connections_but_old_ones_finish():
    lb = LeastConnections({"a": 1, "b": 1})
    old = lb.acquire()
    assert old.server == "a"
    lb.drain("a")
    assert set(route_many(lb, 4)) == {"b"}
    assert lb.remove("a") is False, "a server with active connections cannot be removed yet"
    lb.release(old)
    assert lb.remove("a") is True
    assert lb.snapshot() == {"b": 4}


def test_undrain_and_no_capacity():
    lb = LeastConnections({"a": 1})
    lb.drain("a")
    with pytest.raises(NoCapacity):
        lb.acquire()
    lb.undrain("a")
    assert lb.acquire().server == "a"
    assert lb.total_served == 1


def test_new_server_picks_up_traffic_immediately():
    lb = LeastConnections({"a": 1})
    route_many(lb, 3)
    lb.add("b", 1)
    assert route_many(lb, 4) == ["b", "b", "b", "a"]
