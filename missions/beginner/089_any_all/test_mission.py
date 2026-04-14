import os, sys
sys.path.insert(0, os.path.dirname(__file__))

def test_all_up():
    from broken import all_healthy
    assert all_healthy([{"status":"up"},{"status":"up"}]) is True

def test_one_down():
    from broken import all_healthy
    assert all_healthy([{"status":"up"},{"status":"down"}]) is False

def test_empty():
    from broken import all_healthy
    assert all_healthy([]) is True
