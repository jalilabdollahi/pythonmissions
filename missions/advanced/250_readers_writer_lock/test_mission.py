import os
import sys
import threading
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

from broken import ConfigStore, RWLock


def wait_until(predicate, limit=2.0):
    end = time.monotonic() + limit
    while time.monotonic() < end:
        if predicate():
            return True
        time.sleep(0.002)
    return False


def spawn(fn):
    results = []
    thread = threading.Thread(target=lambda: results.append(fn()), daemon=True)
    thread.start()
    return thread, results


def test_many_readers_share_the_lock():
    lock = RWLock()
    barrier = threading.Barrier(3, timeout=2)

    def reader():
        with lock.reading():
            barrier.wait()  # only passes if all three readers are inside at once
            return "inside"

    spawned = [spawn(reader) for _ in range(3)]
    for thread, _ in spawned:
        thread.join(timeout=3)
    assert [r for _, r in spawned] == [["inside"]] * 3


def test_writer_excludes_readers_and_writers():
    lock = RWLock()
    assert lock.acquire_write()
    assert lock.acquire_read(timeout=0.05) is False
    assert lock.acquire_write(timeout=0.05) is False
    lock.release_write()
    assert lock.acquire_read(timeout=0.05) is True
    assert lock.acquire_write(timeout=0.05) is False
    lock.release_read()
    assert lock.acquire_write(timeout=0.05) is True


def test_waiting_writer_blocks_new_readers():
    lock = RWLock()
    assert lock.acquire_read()
    writer, got = spawn(lambda: lock.acquire_write(timeout=5))
    assert wait_until(lambda: lock.waiting_writers == 1)
    assert lock.acquire_read(timeout=0.1) is False, "new readers must queue behind a waiting writer or it starves"
    lock.release_read()
    writer.join(timeout=1)
    assert got == [True]
    lock.release_write()


def test_all_waiting_readers_wake_when_the_writer_leaves():
    lock = RWLock()
    assert lock.acquire_write()
    spawned = [spawn(lambda: lock.acquire_read(timeout=5)) for _ in range(3)]
    assert wait_until(lambda: lock.waiting_readers == 3)
    lock.release_write()
    for thread, _ in spawned:
        thread.join(timeout=1)
    assert not any(t.is_alive() for t, _ in spawned), "release_write must wake every waiting reader"
    assert [r for _, r in spawned] == [[True]] * 3


def test_timed_out_writer_stops_blocking_readers():
    lock = RWLock()
    assert lock.acquire_read()
    writer, got = spawn(lambda: lock.acquire_write(timeout=0.2))
    assert wait_until(lambda: lock.waiting_writers == 1)
    reader, ok = spawn(lambda: lock.acquire_read(timeout=5))
    assert wait_until(lambda: lock.waiting_readers == 1)
    writer.join(timeout=2)
    assert got == [False]
    reader.join(timeout=1)
    assert not reader.is_alive(), "when the writer gives up, blocked readers must be woken"
    assert ok == [True]
    assert lock.waiting_writers == 0


def test_unbalanced_releases_are_errors():
    lock = RWLock()
    with pytest.raises(RuntimeError):
        lock.release_read()
    with pytest.raises(RuntimeError):
        lock.release_write()
    assert lock.acquire_write(timeout=0.05) is True, "a bad release must not corrupt the reader count"


def test_context_managers_release_on_error_and_report_timeouts():
    lock = RWLock()
    with pytest.raises(ValueError):
        with lock.writing():
            raise ValueError("boom")
    with lock.writing(timeout=0.05):
        with pytest.raises(TimeoutError):
            with lock.reading(timeout=0.05):
                pass


def test_config_store_versions_are_consistent():
    store = ConfigStore({"mode": "blue"})
    assert store.update({"mode": "green", "pool": 8}) == 1
    version, data = store.snapshot()
    assert version == 1 and data == {"mode": "green", "pool": 8}
    assert store.get("mode") == "green" and store.get("missing", "x") == "x"
