import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import broken

ALIVE = lambda pid: pid == 4242
NOBODY = lambda pid: False


def test_acquire_creates_pidfile(tmp_path):
    path = tmp_path / "cinder.pid"
    broken.acquire(path, 100, NOBODY)
    assert path.read_text() == "100"


def test_acquire_refused_when_process_is_alive(tmp_path):
    path = tmp_path / "cinder.pid"
    path.write_text("4242")
    with pytest.raises(broken.AlreadyRunning):
        broken.acquire(path, 100, ALIVE)
    assert path.read_text() == "4242"


def test_stale_pidfile_is_overwritten(tmp_path):
    path = tmp_path / "cinder.pid"
    path.write_text("999")
    broken.acquire(path, 100, ALIVE)
    assert path.read_text() == "100", "pid 999 is dead so the file is stale"


def test_garbage_pidfile_counts_as_stale(tmp_path):
    path = tmp_path / "cinder.pid"
    path.write_text("not-a-pid\n")
    assert broken.read_pid(path) is None
    broken.acquire(path, 7, NOBODY)
    assert path.read_text() == "7"


def test_read_pid_missing_file(tmp_path):
    assert broken.read_pid(tmp_path / "nope.pid") is None


def test_status_values(tmp_path):
    path = tmp_path / "cinder.pid"
    assert broken.status(path, ALIVE) == "stopped"
    path.write_text("4242")
    assert broken.status(path, ALIVE) == "running"
    path.write_text("1")
    assert broken.status(path, ALIVE) == "stale"


def test_release_removes_own_pidfile(tmp_path):
    path = tmp_path / "cinder.pid"
    broken.acquire(path, 55, NOBODY)
    broken.release(path, 55)
    assert not path.exists()


def test_release_leaves_someone_elses_pidfile(tmp_path):
    path = tmp_path / "cinder.pid"
    path.write_text("4242")
    broken.release(path, 100)
    assert path.exists(), "pid 100 never owned this file"
