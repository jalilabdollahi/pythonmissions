import pytest, sys
sys.path.insert(0, ".")
from broken import evaluate_flag, user_bucket

FULL_FLAG = {"enabled": True, "percentage": 100}
HALF_FLAG = {"enabled": True, "percentage": 50}
SEG_FLAG  = {"enabled": True, "percentage": 100, "segments": ["beta"]}

def test_fully_enabled():
    assert evaluate_flag(FULL_FLAG, "user-123") is True

def test_disabled():
    flag = {"enabled": False, "percentage": 100}
    assert evaluate_flag(flag, "user-123") is False

def test_segment_match():
    assert evaluate_flag(SEG_FLAG, "user-123", "beta") is True

def test_segment_mismatch():
    assert evaluate_flag(SEG_FLAG, "user-123", "prod") is False

def test_bucket_range():
    b = user_bucket("any-user")
    assert 0 <= b < 100
