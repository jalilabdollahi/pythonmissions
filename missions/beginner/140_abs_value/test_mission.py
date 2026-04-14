import os, sys
sys.path.insert(0, os.path.dirname(__file__))

def test_positive_delta():
    from broken import disk_delta
    assert disk_delta(480, 500) == 20

def test_negative_becomes_positive():
    from broken import disk_delta
    assert disk_delta(500, 480) == 20

def test_no_change():
    from broken import disk_delta
    assert disk_delta(500, 500) == 0
