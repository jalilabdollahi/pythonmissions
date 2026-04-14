import os, sys
sys.path.insert(0, os.path.dirname(__file__))

def test_healthy():
    from broken import get_status
    assert get_status(200) == "healthy"

def test_unhealthy():
    from broken import get_status
    assert get_status(500) == "unhealthy"

def test_returns_not_none():
    from broken import get_status
    assert get_status(200) is not None
