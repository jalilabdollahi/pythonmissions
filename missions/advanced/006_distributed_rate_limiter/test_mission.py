import pytest, sys
sys.path.insert(0, ".")
from broken import DistributedRateLimiter, FakeRedis

def test_allows_under_limit():
    r = FakeRedis()
    rl = DistributedRateLimiter(r, limit=5, window_seconds=60)
    for _ in range(5):
        assert rl.is_allowed("user-1") is True

def test_blocks_over_limit():
    r = FakeRedis()
    rl = DistributedRateLimiter(r, limit=3, window_seconds=60)
    for _ in range(3):
        rl.is_allowed("user-2")
    assert rl.is_allowed("user-2") is False

def test_different_users_independent():
    r = FakeRedis()
    rl = DistributedRateLimiter(r, limit=2, window_seconds=60)
    rl.is_allowed("user-a"); rl.is_allowed("user-a")
    assert rl.is_allowed("user-b") is True
