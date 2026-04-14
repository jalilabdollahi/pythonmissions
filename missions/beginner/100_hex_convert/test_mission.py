import os, sys
sys.path.insert(0, os.path.dirname(__file__))

def test_converts_correctly():
    from broken import hex_to_int
    assert hex_to_int("#FF5733") == 0xFF5733

def test_without_hash():
    from broken import hex_to_int
    assert hex_to_int("FF5733") == 0xFF5733

def test_zero():
    from broken import hex_to_int
    assert hex_to_int("#000000") == 0
