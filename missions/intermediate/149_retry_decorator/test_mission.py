import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import broken


class Flaky:
    def __init__(self, failures, exc=ConnectionError):
        self.failures = failures
        self.exc = exc
        self.calls = 0

    def __call__(self, *args):
        self.calls += 1
        if self.calls <= self.failures:
            raise self.exc("boom")
        return "ok"


def test_succeeds_after_transient_failures_and_sleeps_between():
    sleeps = []
    f = Flaky(2)
    wrapped = broken.retry(attempts=3, delay=2, sleep=sleeps.append)(f)
    assert wrapped() == "ok"
    assert f.calls == 3
    assert sleeps == [2, 2]


def test_exhausted_attempts_reraise_original_error():
    f = Flaky(10)
    wrapped = broken.retry(attempts=3, sleep=lambda s: None)(f)
    with pytest.raises(ConnectionError):
        wrapped()
    assert f.calls == 3, "the last failure must be raised, not swallowed"


def test_non_retryable_error_is_not_retried():
    f = Flaky(10, exc=ValueError)
    wrapped = broken.retry(attempts=5, sleep=lambda s: None)(f)
    with pytest.raises(ValueError):
        wrapped()
    assert f.calls == 1, "ValueError is not in retry_on so it must propagate at once"


def test_custom_retry_on_tuple_is_respected():
    f = Flaky(1, exc=TimeoutError)
    wrapped = broken.retry(attempts=2, retry_on=(TimeoutError,), sleep=lambda s: None)(f)
    assert wrapped() == "ok"


def test_metadata_is_preserved():
    assert broken.fetch_invoice_batch.__name__ == "fetch_invoice_batch"
    assert broken.fetch_invoice_batch.__doc__ == "Download one batch of invoices."


def test_no_sleep_after_the_final_attempt():
    sleeps = []
    wrapped = broken.retry(attempts=3, sleep=sleeps.append, delay=1)(Flaky(10))
    with pytest.raises(ConnectionError):
        wrapped()
    assert len(sleeps) == 2
