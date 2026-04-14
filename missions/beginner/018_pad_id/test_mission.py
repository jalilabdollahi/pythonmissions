import os, sys
sys.path.insert(0, os.path.dirname(__file__))

def test_small_number():
    from broken import pad_id
    assert pad_id(42) == "000042"

def test_max():
    from broken import pad_id
    assert pad_id(999999) == "999999"

def test_zero():
    from broken import pad_id
    assert pad_id(0) == "000000"

def test_length():
    from broken import pad_id
    assert len(pad_id(1)) == 6
