import pytest, sys, random
sys.path.insert(0, ".")
from broken import CanaryRouter

def test_zero_pct_always_stable():
    router = CanaryRouter("http://stable", "http://canary", canary_pct=0)
    results = {router.route() for _ in range(50)}
    assert results == {"http://stable"}

def test_100_pct_always_canary():
    router = CanaryRouter("http://stable", "http://canary", canary_pct=100)
    results = {router.route() for _ in range(50)}
    assert results == {"http://canary"}

def test_clamped():
    router = CanaryRouter("s", "c", canary_pct=150)
    assert router.canary_pct == 100
