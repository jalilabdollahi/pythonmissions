import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

import broken


def boom():
    raise ValueError("migration failed")


def test_successful_run_returns_results_and_unlocks():
    d = broken.Deployer()
    assert d.run([lambda: 1, lambda: 2]) == [1, 2]
    assert d.is_idle()


def test_failure_propagates_to_caller():
    d = broken.Deployer()
    with pytest.raises(ValueError):
        d.run([boom])


def test_lock_is_released_after_failure():
    d = broken.Deployer()
    with pytest.raises(ValueError):
        d.run([boom])
    assert d.locked is False, "a failed step must not leave the deployer locked"


def test_next_deploy_works_after_failed_one():
    d = broken.Deployer()
    with pytest.raises(ValueError):
        d.run([lambda: "ok", boom])
    assert d.run([lambda: "retry"]) == ["retry"]


def test_concurrent_deploy_is_refused():
    d = broken.Deployer()

    def nested():
        d.run([lambda: 1])

    with pytest.raises(RuntimeError, match="already running"):
        d.run([nested])
    assert d.is_idle()


def test_runs_counter_counts_started_attempts():
    d = broken.Deployer()
    d.run([lambda: 1])
    with pytest.raises(ValueError):
        d.run([boom])
    assert d.runs == 2
