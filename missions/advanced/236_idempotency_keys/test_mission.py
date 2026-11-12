import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import IdempotencyStore, KeyConflict, PayoutService, fingerprint


class Clock:
    def __init__(self):
        self.now = 0.0

    def __call__(self):
        return self.now


def make(ttl=100.0):
    clock = Clock()
    return PayoutService(IdempotencyStore(clock, ttl)), clock


def test_retry_with_same_key_and_payload_replays_the_response():
    svc, _ = make()
    first, replayed1 = svc.create_payout("acme", "k1", {"account": "A", "amount": 50})
    second, replayed2 = svc.create_payout("acme", "k1", {"account": "A", "amount": 50})
    assert (replayed1, replayed2) == (False, True)
    assert first == second
    assert len(svc.ledger) == 1, "the payout must only be made once"


def test_field_order_does_not_change_the_fingerprint():
    assert fingerprint({"a": 1, "b": 2}) == fingerprint({"b": 2, "a": 1})
    svc, _ = make()
    svc.create_payout("acme", "k1", {"account": "A", "amount": 50})
    _, replayed = svc.create_payout("acme", "k1", {"amount": 50, "account": "A"})
    assert replayed is True


def test_same_key_with_different_payload_is_a_conflict():
    svc, _ = make()
    svc.create_payout("acme", "k1", {"account": "A", "amount": 50})
    with pytest.raises(KeyConflict):
        svc.create_payout("acme", "k1", {"account": "A", "amount": 5000})
    assert len(svc.ledger) == 1


def test_tenants_do_not_share_keys():
    svc, _ = make()
    a, _ = svc.create_payout("acme", "k1", {"account": "A", "amount": 50})
    b, replayed = svc.create_payout("globex", "k1", {"account": "G", "amount": 70})
    assert replayed is False and b != a, "another tenant's receipt must never be returned"
    assert len(svc.ledger) == 2


def test_failed_handler_releases_the_key_for_retry():
    store = IdempotencyStore(Clock())
    calls = []

    def flaky(payload):
        calls.append(payload)
        if len(calls) == 1:
            raise TimeoutError("bank timeout")
        return {"ok": True}

    with pytest.raises(TimeoutError):
        store.execute("acme", "k1", {"x": 1}, flaky)
    assert store.size() == 0
    assert store.execute("acme", "k1", {"x": 1}, flaky) == ({"ok": True}, False)


def test_request_while_in_flight_is_rejected():
    store = IdempotencyStore(Clock())

    def reentrant(payload):
        with pytest.raises(KeyConflict):
            store.execute("acme", "k1", payload, lambda p: None)
        return "done"

    assert store.execute("acme", "k1", {"x": 1}, reentrant) == ("done", False)


def test_status_and_forget_tenant():
    svc, _ = make()
    svc.create_payout("acme", "k1", {"account": "A", "amount": 1})
    svc.create_payout("acme", "k2", {"account": "A", "amount": 2})
    svc.create_payout("globex", "k1", {"account": "G", "amount": 3})
    assert svc.store.status("acme", "k1") == "done"
    assert svc.store.status("acme", "nope") is None
    assert svc.store.forget_tenant("acme") == 2
    assert svc.store.size() == 1


def test_records_expire_after_ttl():
    svc, clock = make(ttl=100.0)
    svc.create_payout("acme", "k1", {"account": "A", "amount": 1})
    clock.now = 99.9
    assert svc.create_payout("acme", "k1", {"account": "A", "amount": 1})[1] is True
    clock.now = 100.0
    assert svc.create_payout("acme", "k1", {"account": "A", "amount": 1})[1] is False
    assert len(svc.ledger) == 2
