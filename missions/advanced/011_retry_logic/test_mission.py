import os
import sys
import pytest

sys.path.insert(0, os.path.dirname(__file__))


def test_wrapper_preserves_function_name():
    from broken import retry

    @retry(max_attempts=2, delay=0)
    def my_function():
        """My docstring."""
        pass

    assert my_function.__name__ == "my_function"


def test_wrapper_preserves_docstring():
    from broken import retry

    @retry(max_attempts=2, delay=0)
    def documented():
        """Important docstring."""
        pass

    assert documented.__doc__ == "Important docstring."


def test_retries_correct_number_of_times():
    from broken import retry
    calls = []

    @retry(max_attempts=3, delay=0)
    def flaky():
        calls.append(1)
        raise ValueError("fail")

    with pytest.raises(ValueError):
        flaky()

    assert len(calls) == 3


def test_returns_value_on_success():
    from broken import retry

    @retry(max_attempts=3, delay=0)
    def stable():
        return 42

    assert stable() == 42


def test_retries_until_success():
    from broken import retry
    attempts = []

    @retry(max_attempts=5, delay=0)
    def eventually_works():
        attempts.append(1)
        if len(attempts) < 3:
            raise IOError("not yet")
        return "ok"

    result = eventually_works()
    assert result == "ok"
    assert len(attempts) == 3


def test_no_sleep_after_last_attempt():
    from broken import retry

    sleep_calls = []

    @retry(max_attempts=3, delay=60)
    def always_fails():
        raise RuntimeError("fail")

    import broken

    original_sleep = broken.time.sleep

    def fake_sleep(delay):
        sleep_calls.append(delay)

    broken.time.sleep = fake_sleep
    try:
        with pytest.raises(RuntimeError):
            always_fails()
    finally:
        broken.time.sleep = original_sleep

    assert sleep_calls == [60, 60]


def test_raises_last_exception():
    from broken import retry

    @retry(max_attempts=2, delay=0)
    def fails_with_value_error():
        raise ValueError("specific error")

    with pytest.raises(ValueError, match="specific error"):
        fails_with_value_error()
