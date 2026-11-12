import os
import sys
import threading

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

from broken import CapExceeded, InsufficientQuota, QuotaLedger, Tenant


def make_ledger():
    return QuotaLedger([Tenant("acme", 100, 500), Tenant("globex", 100, 500), Tenant("initech", 10, 50)])


def start(fn, *args):
    outcome = []

    def body():
        try:
            fn(*args)
            outcome.append("ok")
        except Exception as exc:
            outcome.append(type(exc).__name__)

    thread = threading.Thread(target=body, daemon=True)
    thread.start()
    return thread, outcome


def barrier_hook(stage_name, parties=2):
    barrier = threading.Barrier(parties)

    def hook(stage):
        if stage == stage_name:
            try:
                barrier.wait(timeout=0.3)
            except threading.BrokenBarrierError:
                pass

    return hook


def test_simple_transfer_moves_quota():
    ledger = make_ledger()
    ledger.transfer("acme", "globex", 30)
    assert ledger.audit() == {"acme": 70, "globex": 130, "initech": 10}
    assert ledger.history == [("acme", "globex", 30)]
    assert ledger.headroom("globex") == 370


def test_opposite_transfers_do_not_deadlock():
    ledger = make_ledger()
    ledger.hook = barrier_hook("first_locked")
    t1, r1 = start(ledger.transfer, "acme", "globex", 10)
    t2, r2 = start(ledger.transfer, "globex", "acme", 20)
    t1.join(timeout=2)
    t2.join(timeout=2)
    assert not t1.is_alive() and not t2.is_alive(), "A->B and B->A deadlock unless locks are taken in one global order"
    assert r1 == ["ok"] and r2 == ["ok"]
    assert ledger.audit() == {"acme": 110, "globex": 90, "initech": 10}


def test_transfer_to_self_is_rejected_instead_of_hanging():
    ledger = make_ledger()
    thread, outcome = start(ledger.transfer, "acme", "acme", 5)
    thread.join(timeout=1)
    assert not thread.is_alive(), "taking the same non-reentrant lock twice hangs forever"
    assert outcome == ["ValueError"]


def test_balance_is_checked_while_holding_the_locks():
    ledger = make_ledger()
    ledger.hook = barrier_hook("validated")
    t1, r1 = start(ledger.transfer, "acme", "globex", 60)
    t2, r2 = start(ledger.transfer, "acme", "globex", 50)
    t1.join(timeout=2)
    t2.join(timeout=2)
    assert sorted(r1 + r2) == ["InsufficientQuota", "ok"], "both transfers saw 100 units and both went through"
    audit = ledger.audit()
    assert audit["acme"] >= 0, "quota must never go negative"
    assert sum(audit.values()) == 210


def test_cap_violation_leaves_both_tenants_untouched():
    ledger = make_ledger()
    with pytest.raises(CapExceeded):
        ledger.transfer("acme", "initech", 41)
    assert ledger.audit() == {"acme": 100, "globex": 100, "initech": 10}, "a rejected transfer must not lose quota"
    assert ledger.history == []


def test_insufficient_quota_and_bad_units():
    ledger = make_ledger()
    with pytest.raises(InsufficientQuota):
        ledger.transfer("initech", "acme", 11)
    with pytest.raises(ValueError):
        ledger.transfer("acme", "globex", 0)
    assert ledger.total() == 210


def test_many_threads_keep_the_total_constant():
    ledger = make_ledger()
    threads = []
    for i in range(12):
        src, dst = ("acme", "globex") if i % 2 else ("globex", "acme")
        thread, _ = start(ledger.transfer, src, dst, 3)
        threads.append(thread)
    for thread in threads:
        thread.join(timeout=2)
    assert not any(t.is_alive() for t in threads)
    assert ledger.total() == 210
    assert len(ledger.history) == 12


def test_transfer_many_reports_rejections_and_keeps_going():
    ledger = make_ledger()
    results = ledger.transfer_many([("acme", "globex", 50), ("initech", "acme", 99), ("globex", "initech", 45)])
    assert results == ["ok", "InsufficientQuota", "CapExceeded"]
    assert ledger.audit() == {"acme": 50, "globex": 150, "initech": 10}
