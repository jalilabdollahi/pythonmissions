import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

from broken import KeyStore, rotation_report, sign, verify


def rotated_store(grace=600):
    store = KeyStore(grace=grace)
    store.add("k1", "alpha-secret", 0)
    store.add("k2", "beta-secret", 1000)
    return store


def test_signing_uses_the_newest_active_key_not_the_oldest():
    store = rotated_store()
    assert sign(store, "pay", now=500)[0] == "k1"
    assert sign(store, "pay", now=1200)[0] == "k2", "during the overlap new tokens must use the new key"


def test_old_signatures_survive_the_overlap_window():
    store = rotated_store()
    key_id, sig = sign(store, "order-42", now=900)
    assert verify(store, "order-42", key_id, sig, now=1500), "grace period covers in-flight requests"


def test_old_key_stops_verifying_exactly_when_grace_ends():
    store = rotated_store(grace=600)
    key_id, sig = sign(store, "order-42", now=900)
    assert verify(store, "order-42", key_id, sig, now=1599)
    assert not verify(store, "order-42", key_id, sig, now=1600), "retire time is exclusive"
    assert not verify(store, "order-42", key_id, sig, now=5000)


def test_pre_published_key_is_not_valid_before_activation():
    store = rotated_store()
    forged = sign(store, "x", now=1000)[1]
    assert not verify(store, "x", "k2", forged, now=500), "a key that is not active yet cannot vouch for anything"


def test_tampered_payload_or_wrong_key_id_fails():
    store = rotated_store()
    key_id, sig = sign(store, "amount=10", now=1100)
    assert verify(store, "amount=10", key_id, sig, now=1100)
    assert not verify(store, "amount=99", key_id, sig, now=1100)
    assert not verify(store, "amount=10", "k1", sig, now=1100)
    assert not verify(store, "amount=10", "nope", sig, now=1100)


def test_revoked_key_is_rejected_even_inside_the_grace_window():
    store = rotated_store()
    key_id, sig = sign(store, "p", now=900)
    store.revoke("k1")
    assert not verify(store, "p", key_id, sig, now=1100), "compromised keys get no grace"


def test_revoked_current_key_is_never_chosen_for_signing():
    store = rotated_store()
    store.revoke("k2")
    assert sign(store, "p", now=2000)[0] == "k1", "fall back to the newest key that is still trusted"
    store.revoke("k1")
    with pytest.raises(LookupError):
        sign(store, "p", now=2000)


def test_rotation_report_labels_each_phase():
    store = rotated_store()
    store.add("k3", "gamma-secret", 5000)
    assert rotation_report(store, 1200) == {"k1": "retiring", "k2": "active", "k3": "pending"}
    assert rotation_report(store, 3000) == {"k1": "retired", "k2": "active", "k3": "pending"}
    store.revoke("k2")
    assert rotation_report(store, 3000)["k2"] == "revoked"
