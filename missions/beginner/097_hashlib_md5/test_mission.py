import os, sys
sys.path.insert(0, os.path.dirname(__file__))

def test_returns_string():
    from broken import hash_content
    assert isinstance(hash_content("hello"), str)

def test_correct_length():
    from broken import hash_content
    assert len(hash_content("hello")) == 32

def test_deterministic():
    from broken import hash_content
    assert hash_content("hello") == hash_content("hello")

def test_different_inputs():
    from broken import hash_content
    assert hash_content("hello") != hash_content("world")
