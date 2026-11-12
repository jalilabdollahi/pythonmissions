import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import Bulkhead, BulkheadFull


def test_limit_is_exact():
    door = Bulkhead({"seatmap": 2})
    assert [door.acquire("seatmap") for _ in range(3)] == [True, True, False]
    assert door.rejected["seatmap"] == 1
    assert door.peak["seatmap"] == 2


def test_compartments_are_isolated():
    door = Bulkhead({"seatmap": 1, "pricing": 1})
    assert door.acquire("seatmap")
    assert not door.acquire("seatmap")
    assert door.acquire("pricing"), "a full seat-map must not affect pricing"


def test_guard_releases_when_the_call_raises():
    door = Bulkhead({"pricing": 1})
    for _ in range(3):
        try:
            with door.guard("pricing"):
                raise RuntimeError("engine crashed")
        except RuntimeError:
            pass
    assert door.in_flight["pricing"] == 0, "crashes must not leak slots"
    with door.guard("pricing"):
        pass


def test_guard_raises_bulkhead_full_when_busy():
    door = Bulkhead({"pricing": 1})
    with door.guard("pricing"):
        try:
            with door.guard("pricing"):
                raise AssertionError("second entry should have been rejected")
        except BulkheadFull as exc:
            assert exc.dependency == "pricing"


def test_extra_release_cannot_create_capacity():
    door = Bulkhead({"pricing": 1})
    door.release("pricing")
    door.release("pricing")
    assert door.in_flight["pricing"] == 0
    assert door.acquire("pricing")
    assert not door.acquire("pricing"), "limit is still 1 after stray releases"


def test_dependencies_in_one_pool_share_a_limit():
    door = Bulkhead({"db": 2}, pools={"db-primary": "db", "db-replica": "db"})
    assert door.acquire("db-primary")
    assert door.acquire("db-replica")
    assert not door.acquire("db-primary"), "primary and replica share the 2 db slots"
    assert door.report()["db"] == {"in_flight": 2, "rejected": 1, "peak": 2}


def test_unknown_dependency_uses_the_default_and_fallback_runs():
    door = Bulkhead({}, default_limit=1)
    with door.guard("geocoder"):
        assert door.call("geocoder", lambda: "live", fallback=lambda: "cached") == "cached"
    assert door.call("geocoder", lambda: "live", fallback=lambda: "cached") == "live"
