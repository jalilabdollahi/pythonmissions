import pytest, sys
sys.path.insert(0, ".")
from broken import chaos

def test_zero_probability_never_fails():
    @chaos(probability=0.0)
    def stable(): return "ok"
    for _ in range(50):
        assert stable() == "ok"

def test_full_probability_always_fails():
    @chaos(probability=1.0)
    def unstable(): return "ok"
    with pytest.raises(Exception):
        unstable()

def test_custom_exception():
    @chaos(probability=1.0, exception=ValueError, message="test")
    def fn(): return True
    with pytest.raises(ValueError, match="test"):
        fn()
