import pytest
import sys
sys.path.insert(0, ".")
from broken import TokenBucket

def test_initial_tokens():
    b = TokenBucket(10, 1)
    assert b.available() == 10

def test_consume():
    b = TokenBucket(10, 1)
    assert b.consume(5) is True
    assert b.available() == 5

def test_no_overflow():
    b = TokenBucket(10, 1000)
    import time
    time.sleep(0.01)
    assert b.available() <= 10

def test_deny_when_empty():
    b = TokenBucket(2, 0)
    b.consume(2)
    assert b.consume(1) is False
