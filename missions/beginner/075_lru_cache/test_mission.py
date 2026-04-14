import os, sys
sys.path.insert(0, os.path.dirname(__file__))

def test_returns_value():
    from broken import cached_get
    cached_get.cache_clear()
    assert cached_get("host") == "localhost"

def test_caches_result():
    from broken import cached_get
    cached_get.cache_clear()
    cached_get("host")
    cached_get("host")
    assert cached_get.cache_info().hits >= 1

def test_missing_key():
    from broken import cached_get
    cached_get.cache_clear()
    assert cached_get("missing") is None
