import os, sys
sys.path.insert(0, os.path.dirname(__file__))

def test_inserts_correctly():
    from broken import add_threshold
    t = [70, 80, 90]
    add_threshold(t, 85)
    assert t == [70, 80, 85, 90]

def test_inserts_at_start():
    from broken import add_threshold
    t = [70, 80, 90]
    add_threshold(t, 60)
    assert t[0] == 60
