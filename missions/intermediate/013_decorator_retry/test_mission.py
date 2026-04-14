import pytest
import sys
sys.path.insert(0, ".")
from broken import retry

def test_retry_success():
    calls = []
    @retry(max_attempts=3, delay=0)
    def flaky(x):
        calls.append(x)
        if len(calls) < 2:
            raise ValueError("not yet")
        return x * 2
    result = flaky(5)
    assert result == 10

def test_retry_exhausted():
    @retry(max_attempts=2, delay=0)
    def always_fails():
        raise RuntimeError("boom")
    with pytest.raises(RuntimeError):
        always_fails()
