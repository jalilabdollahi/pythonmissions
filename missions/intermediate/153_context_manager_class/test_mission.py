import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import broken


def test_lock_file_exists_inside_block_and_is_removed_after(tmp_path):
    path = tmp_path / "deploy.lock"
    with broken.DeployLock(path, "alice"):
        assert broken.current_owner(path) == "alice"
    assert not path.exists()


def test_enter_returns_the_lock_object(tmp_path):
    with broken.DeployLock(tmp_path / "l", "bob") as lock:
        assert lock is not None, "__enter__ must return self"
        assert lock.owner == "bob"


def test_exception_propagates_out_of_the_block(tmp_path):
    with pytest.raises(RuntimeError, match="migration failed"):
        with broken.DeployLock(tmp_path / "l", "carol"):
            raise RuntimeError("migration failed")


def test_lock_is_released_when_the_block_raises(tmp_path):
    path = tmp_path / "l"
    with pytest.raises(ValueError):
        with broken.DeployLock(path, "dave"):
            raise ValueError("bad build")
    assert not path.exists(), "a failed deploy must not leave a stale lock"


def test_second_acquire_is_refused(tmp_path):
    path = tmp_path / "l"
    with broken.DeployLock(path, "erin"):
        with pytest.raises(broken.LockHeld):
            with broken.DeployLock(path, "frank"):
                pass


def test_failed_acquire_does_not_remove_the_owners_lock(tmp_path):
    path = tmp_path / "l"
    with broken.DeployLock(path, "erin"):
        with pytest.raises(broken.LockHeld):
            with broken.DeployLock(path, "frank"):
                pass
        assert broken.current_owner(path) == "erin", "frank never owned the lock"


def test_lock_can_be_taken_again_after_release(tmp_path):
    path = tmp_path / "l"
    with broken.DeployLock(path, "a"):
        pass
    with broken.DeployLock(path, "b"):
        assert broken.current_owner(path) == "b"
