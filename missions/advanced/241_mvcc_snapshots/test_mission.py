import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

from broken import MVCCStore, WriteConflict


def seeded(**rows):
    store = MVCCStore()
    txn = store.begin()
    for key, value in rows.items():
        store.put(txn, key, value)
    store.commit(txn)
    return store


def test_reader_sees_commit_made_before_it_began():
    store = seeded(acct=100)
    reader = store.begin()
    assert store.get(reader, "acct") == 100, "a snapshot includes every commit with ts <= snapshot"


def test_snapshot_does_not_see_later_commits():
    store = seeded(acct=100)
    reader = store.begin()
    writer = store.begin()
    store.put(writer, "acct", 70)
    store.commit(writer)
    assert store.get(reader, "acct") == 100, "repeatable read: later commits stay invisible"
    assert store.get(store.begin(), "acct") == 70


def test_uncommitted_writes_are_private_to_their_transaction():
    store = seeded(acct=100)
    writer = store.begin()
    other = store.begin()
    store.put(writer, "acct", 55)
    assert store.get(writer, "acct") == 55, "a transaction reads its own writes"
    assert store.get(other, "acct") == 100, "nobody else may see uncommitted data"


def test_own_delete_hides_the_row_from_the_deleter():
    store = seeded(acct=100)
    txn = store.begin()
    assert store.delete(txn, "acct") is True
    assert store.get(txn, "acct") is None, "after my own delete the row must read as gone"
    assert store.get(store.begin(), "acct") == 100


def test_delete_committed_after_snapshot_keeps_row_visible_to_old_reader():
    store = seeded(acct=100)
    reader = store.begin()
    killer = store.begin()
    store.delete(killer, "acct")
    store.commit(killer)
    assert store.get(reader, "acct") == 100
    assert store.get(store.begin(), "acct") is None


def test_concurrent_writers_to_same_row_conflict():
    store = seeded(acct=100)
    first = store.begin()
    second = store.begin()
    store.put(first, "acct", 90)
    with pytest.raises(WriteConflict):
        store.put(second, "acct", 80)
    store.commit(first)
    assert store.get(store.begin(), "acct") == 90, "no lost update"


def test_aborted_transaction_leaves_no_trace():
    store = seeded(acct=100, other=1)
    txn = store.begin()
    store.put(txn, "acct", 1)
    store.delete(txn, "other")
    store.abort(txn)
    check = store.begin()
    assert store.get(check, "acct") == 100
    assert store.get(check, "other") == 1, "an aborted delete must be undone"
    retry = store.begin()
    store.put(retry, "acct", 95)
    store.commit(retry)


def test_vacuum_keeps_versions_that_an_open_snapshot_still_needs():
    store = seeded(acct=100)
    old_reader = store.begin()
    writer = store.begin()
    store.put(writer, "acct", 60)
    store.commit(writer)
    young_reader = store.begin()
    assert store.vacuum() == 0, "the old version is still visible to old_reader"
    assert store.get(old_reader, "acct") == 100
    assert store.get(young_reader, "acct") == 60
    store.commit(old_reader)
    store.commit(young_reader)
    assert store.vacuum() == 1, "once nobody can see it, the old version is garbage"
    assert store.get(store.begin(), "acct") == 60


def test_update_conflicts_with_an_in_flight_delete():
    store = seeded(acct=100)
    killer = store.begin()
    updater = store.begin()
    assert store.delete(killer, "acct") is True
    with pytest.raises(WriteConflict):
        store.put(updater, "acct", 50)
    with pytest.raises(WriteConflict):
        store.delete(updater, "acct")
