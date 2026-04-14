import os, sys, time
sys.path.insert(0, os.path.dirname(__file__))

def test_returns_small_elapsed():
    from broken import elapsed_seconds
    start = time.time()
    elapsed = elapsed_seconds(start)
    assert 0 <= elapsed < 1

def test_elapsed_positive():
    from broken import elapsed_seconds
    start = time.time() - 5
    assert elapsed_seconds(start) >= 5
