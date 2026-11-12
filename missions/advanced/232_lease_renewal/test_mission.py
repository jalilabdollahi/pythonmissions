import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import Elector, LeaseStore, dispatch


class Clock:
    def __init__(self):
        self.now = 500.0

    def __call__(self):
        return self.now

    def advance(self, seconds):
        self.now += seconds


def make(latency=0.0):
    clock = Clock()
    store = LeaseStore(clock, latency=latency, sleep=clock.advance)
    a = Elector("sched-a", store, clock)
    b = Elector("sched-b", store, clock)
    return clock, store, a, b


def test_first_instance_becomes_leader_second_does_not():
    clock, store, a, b = make()
    assert a.tick() is True
    assert b.tick() is False
    assert dispatch(a, ["j1"]) == ["sched-a:j1"] and dispatch(b, ["j1"]) == []


def test_leader_renews_on_schedule_and_keeps_the_lease():
    clock, store, a, b = make()
    a.tick()
    for _ in range(6):
        clock.advance(5)
        assert a.tick() is True, "renewing every 5s must keep a 15s lease alive"
        assert b.tick() is False


def test_local_deadline_is_measured_from_before_the_slow_call():
    clock, store, a, b = make(latency=4.0)
    a.tick()
    clock.now = 505.0
    assert a.tick() is True
    assert store.expires_at == 505.0 + 4.0 + 15, "store stamps the lease after its 4s delay"
    assert a.deadline == 505.0 + 15 - 2, "leader must count from when it SENT the renewal"
    assert a.deadline < store.expires_at


def test_leader_stops_exactly_at_deadline():
    clock, store, a, b = make()
    a.tick()
    clock.now = a.deadline
    assert not a.is_leader(), "deadline is exclusive: now == deadline means stop"


def test_new_leader_can_only_take_over_after_store_expiry():
    clock, store, a, b = make()
    a.tick()
    clock.now = store.expires_at - 0.01
    assert b.tick() is False
    clock.now = store.expires_at
    assert b.tick() is True, "now >= expires_at is free"


def test_a_stale_node_cannot_renew_someone_elses_lease():
    clock, store, a, b = make()
    a.tick()
    clock.now = store.expires_at + 1
    b.tick()
    owner_expiry = store.expires_at
    assert store.renew("sched-a", 15) is False
    assert store.owner == "sched-b" and store.expires_at == owner_expiry


def test_refused_renewal_steps_down_immediately():
    clock, store, a, b = make()
    a.tick()
    clock.now += 5
    store.owner = "sched-b"
    store.expires_at = clock() + 20
    assert a.tick() is False
    assert a.deadline is None and dispatch(a, ["j"]) == [], "no dispatching after losing the lease"
