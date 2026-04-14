import pytest, sys
sys.path.insert(0, ".")
from broken import ReplicationLog, ReplicaApplier

def test_apply_in_order():
    applier = ReplicaApplier()
    entries = [
        {"lsn": 2, "op": "set", "data": {"key": "b", "value": 2}},
        {"lsn": 1, "op": "set", "data": {"key": "a", "value": 1}},
    ]
    gaps = applier.apply_batch(entries)
    assert applier._state == {"a": 1, "b": 2}
    assert gaps == []

def test_detects_gap():
    applier = ReplicaApplier()
    entries = [
        {"lsn": 3, "op": "set", "data": {"key": "c", "value": 3}},
    ]
    gaps = applier.apply_batch(entries)
    assert 1 in gaps  # expected lsn 1 but got 3
