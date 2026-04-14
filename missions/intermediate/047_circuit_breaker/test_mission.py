import pytest
import sys
sys.path.insert(0, ".")
from broken import CircuitBreaker

def test_closes_on_success():
    cb = CircuitBreaker(threshold=3)
    cb.state = cb.HALF_OPEN
    cb.call(lambda: True)
    assert cb.state == cb.CLOSED
    assert cb.failures == 0

def test_opens_after_threshold():
    cb = CircuitBreaker(failure_threshold=3)
    def fail(): raise ValueError("boom")
    for _ in range(3):
        try: cb.call(fail)
        except: pass
    assert cb.state == cb.OPEN

def test_open_raises():
    cb = CircuitBreaker()
    cb.state = cb.OPEN
    cb.last_failure_time = float("inf")
    with pytest.raises(RuntimeError):
        cb.call(lambda: True)
