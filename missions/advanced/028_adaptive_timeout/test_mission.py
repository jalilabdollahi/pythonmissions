import pytest, sys
sys.path.insert(0, ".")
from broken import AdaptiveTimeout

def test_ewma_converges():
    at = AdaptiveTimeout(alpha=0.5)
    for _ in range(100):
        at.record_latency(1.0)
    assert abs(at._ewma - 1.0) < 0.01

def test_ewma_responds_to_spike():
    at = AdaptiveTimeout(alpha=0.5)
    for _ in range(50):
        at.record_latency(0.1)
    at.record_latency(10.0)
    assert at._ewma > 0.1  # EWMA should increase

def test_get_timeout_reasonable():
    at = AdaptiveTimeout()
    for i in range(100):
        at.record_latency(0.1 + i * 0.001)
    timeout = at.get_timeout()
    assert at.min_timeout <= timeout <= at.max_timeout
