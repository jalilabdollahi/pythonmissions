import os, sys
sys.path.insert(0, os.path.dirname(__file__))

def test_a_to_b():
    from broken import next_code
    assert next_code("a") == "b"

def test_d_to_e():
    from broken import next_code
    assert next_code("d") == "e"

def test_returns_string():
    from broken import next_code
    assert isinstance(next_code("a"), str)
