import os, sys
sys.path.insert(0, os.path.dirname(__file__))

def test_two_errors():
    from broken import count_errors
    assert count_errors("ERROR: disk full\nINFO: ok\nERROR: OOM\n") == 2

def test_no_errors():
    from broken import count_errors
    assert count_errors("INFO: all good\nWARN: high cpu\n") == 0

def test_one_error():
    from broken import count_errors
    assert count_errors("ERROR: timeout\n") == 1
