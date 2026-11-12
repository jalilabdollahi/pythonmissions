import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

from broken import DEFAULT_LIMITS, QuotaExceeded, QuotaManager, Tenant


def test_reserving_within_limits_and_exceeding_them():
    t = Tenant("a", {"cpu": 4})
    t.reserve({"cpu": 3})
    assert t.available("cpu") == 1
    with pytest.raises(QuotaExceeded) as info:
        t.reserve({"cpu": 2})
    assert info.value.resource == "cpu"
    assert t.used["cpu"] == 3


def test_overriding_one_tenant_does_not_change_the_defaults_or_other_tenants():
    mgr = QuotaManager()
    mgr.register("big", {"cpu": 64})
    small = mgr.register("small")
    assert DEFAULT_LIMITS["cpu"] == 16, "tenant limits must be copies of the defaults"
    assert small.limits["cpu"] == 16


def test_usage_is_tracked_per_tenant():
    mgr = QuotaManager()
    mgr.register("a")
    mgr.register("b")
    mgr.reserve("a", {"cpu": 10})
    assert mgr.tenants["b"].used["cpu"] == 0
    with pytest.raises(QuotaExceeded):
        mgr.reserve("a", {"cpu": 7})
    mgr.reserve("b", {"cpu": 16})


def test_history_is_private_to_each_tenant():
    a = Tenant("a")
    b = Tenant("b")
    a.reserve({"cpu": 1})
    assert b.history == [], "one tenant must never see another tenant's audit trail"
    assert a.history == [("reserve", {"cpu": 1})]


def test_failed_multi_resource_reservation_changes_nothing():
    t = Tenant("a", {"cpu": 8, "memory_gb": 8})
    with pytest.raises(QuotaExceeded):
        t.reserve({"cpu": 4, "memory_gb": 100})
    assert t.used == {"cpu": 0, "memory_gb": 0, "disks": 0}, "all-or-nothing: no partial reservation"
    assert t.history == []


def test_releasing_more_than_reserved_cannot_create_phantom_capacity():
    t = Tenant("a", {"cpu": 4})
    t.reserve({"cpu": 2})
    t.release({"cpu": 5})
    assert t.used["cpu"] == 0
    assert t.available("cpu") == 4, "usage cannot go negative, otherwise the limit is silently raised"
    with pytest.raises(QuotaExceeded):
        t.reserve({"cpu": 5})


def test_invalid_requests_are_rejected_before_any_change():
    t = Tenant("a")
    with pytest.raises(ValueError):
        t.reserve({"cpu": 1, "disks": -1})
    with pytest.raises(KeyError):
        t.reserve({"cpu": 1, "gpu": 1})
    assert t.used["cpu"] == 0


def test_utilization_and_noisy_neighbours():
    mgr = QuotaManager()
    mgr.register("quiet", {"cpu": 10})
    mgr.register("loud", {"cpu": 10})
    mgr.reserve("quiet", {"cpu": 2})
    mgr.reserve("loud", {"cpu": 9})
    assert mgr.tenants["loud"].utilization()["cpu"] == 0.9
    assert mgr.noisy_tenants() == ["loud"]
    with pytest.raises(ValueError):
        mgr.register("loud")
