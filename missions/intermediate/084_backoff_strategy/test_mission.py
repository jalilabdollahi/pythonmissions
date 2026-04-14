import pytest, sys
sys.path.insert(0, ".")
from broken import backoff_delay, should_retry

def test_exponential_growth():
    d0 = backoff_delay(0, base=1.0, jitter=False)
    d1 = backoff_delay(1, base=1.0, jitter=False)
    d2 = backoff_delay(2, base=1.0, jitter=False)
    assert d0 == 1.0
    assert d1 == 2.0
    assert d2 == 4.0

def test_cap():
    d = backoff_delay(100, base=1.0, cap=60.0, jitter=False)
    assert d == 60.0

def test_jitter_adds():
    delays = [backoff_delay(3, base=0.1) for _ in range(10)]
    assert len(set(delays)) > 1  # jitter produces variation
