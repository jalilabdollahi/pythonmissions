import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

from broken import Registry


class Clock:
    def __init__(self):
        self.now = 100.0

    def __call__(self):
        return self.now


def setup(default_ttl=30.0):
    clock = Clock()
    return clock, Registry(clock, default_ttl)


def test_registered_instances_are_found_until_their_ttl_runs_out():
    clock, reg = setup()
    reg.register("billing", "b-1", "10.0.0.1:8080")
    reg.register("billing", "b-2", "10.0.0.2:8080")
    assert reg.lookup("billing") == ["10.0.0.1:8080", "10.0.0.2:8080"]
    clock.now += 29.9
    assert reg.lookup("billing") == ["10.0.0.1:8080", "10.0.0.2:8080"]
    assert reg.services() == ["billing"]


def test_instance_expires_exactly_at_its_deadline():
    clock, reg = setup()
    reg.register("billing", "b-1", "10.0.0.1:8080")
    clock.now += 30.0
    assert reg.lookup("billing") == [], "an instance whose TTL has fully elapsed is gone"
    assert reg.services() == []
    assert reg.ttl_remaining("billing", "b-1") == 0.0


def test_heartbeat_extends_the_lease_using_the_instance_ttl():
    clock, reg = setup(default_ttl=30.0)
    reg.register("search", "s-1", "10.0.1.1:9200", ttl=5.0)
    clock.now += 4.0
    assert reg.heartbeat("search", "s-1") is True
    assert reg.ttl_remaining("search", "s-1") == 5.0, "this instance asked for a 5 second lease, not the default"
    clock.now += 6.0
    assert reg.lookup("search") == []


def test_heartbeat_cannot_resurrect_an_expired_instance():
    clock, reg = setup()
    reg.register("billing", "b-1", "10.0.0.1:8080")
    clock.now += 45.0
    assert reg.heartbeat("billing", "b-1") is False, "a late heartbeat means the instance must register again"
    assert reg.lookup("billing") == []
    assert ("expired", "billing", "b-1") in reg.events
    assert reg.heartbeat("billing", "unknown") is False


def test_reregistering_replaces_the_old_entry():
    clock, reg = setup()
    reg.register("billing", "b-1", "10.0.0.1:8080")
    reg.register("billing", "b-1", "10.0.0.1:9090")
    assert reg.lookup("billing") == ["10.0.0.1:9090"], "a restarted instance must not leave a ghost behind"


def test_deregister_and_sweep_emit_events():
    clock, reg = setup()
    reg.register("api", "a-1", "10.0.2.1:80", ttl=10.0)
    reg.register("api", "a-2", "10.0.2.2:80", ttl=60.0)
    reg.register("api", "a-3", "10.0.2.3:80", ttl=60.0)
    assert reg.deregister("api", "a-3") is True
    assert reg.deregister("api", "a-3") is False
    clock.now += 11.0
    assert reg.sweep() == [("api", "a-1")]
    assert reg.lookup("api") == ["10.0.2.2:80"]
    assert [e for e in reg.events if e[0] != "up"] == [("down", "api", "a-3"), ("expired", "api", "a-1")]


def test_lookup_by_tag_and_validation():
    clock, reg = setup()
    reg.register("db", "d-1", "10.0.3.1:5432", tags=["primary"])
    reg.register("db", "d-2", "10.0.3.2:5432", tags=["replica"])
    assert reg.lookup("db", tag="replica") == ["10.0.3.2:5432"]
    with pytest.raises(ValueError):
        reg.register("db", "d-3", "10.0.3.3:5432", ttl=0)
