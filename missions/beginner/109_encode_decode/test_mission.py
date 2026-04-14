import os, sys
sys.path.insert(0, os.path.dirname(__file__))

def test_to_bytes():
    from broken import to_bytes
    assert to_bytes("hello") == b"hello"

def test_to_string():
    from broken import to_string
    assert to_string(b"hello") == "hello"

def test_roundtrip():
    from broken import to_bytes, to_string
    assert to_string(to_bytes("deploy complete")) == "deploy complete"
