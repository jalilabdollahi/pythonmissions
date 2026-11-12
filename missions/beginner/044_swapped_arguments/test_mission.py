import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import check_database, check_registry, run_probe


class RecordingOpener:
    def __init__(self, fail=True):
        self.fail = fail
        self.timeouts = []

    def __call__(self, url, timeout):
        self.timeouts.append(timeout)
        if self.fail:
            raise ConnectionError("down")
        return "pong"


def test_registry_tries_three_times():
    opener = RecordingOpener()
    assert check_registry("https://registry", opener) is False
    assert len(opener.timeouts) == 3, "registry policy is 3 retries"


def test_registry_timeout_is_thirty_seconds():
    opener = RecordingOpener()
    check_registry("https://registry", opener)
    assert set(opener.timeouts) == {30}


def test_database_policy():
    opener = RecordingOpener()
    check_database("db://main", opener)
    assert opener.timeouts == [10, 10], "database: 2 retries with a 10 second timeout"


def test_success_returns_true_after_one_call():
    opener = RecordingOpener(fail=False)
    assert check_registry("https://registry", opener) is True
    assert len(opener.timeouts) == 1


def test_run_probe_defaults():
    opener = RecordingOpener()
    run_probe("x", opener)
    assert opener.timeouts == [5]
