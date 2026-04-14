import os, sys
sys.path.insert(0, os.path.dirname(__file__))

def test_joins_with_pipe():
    from broken import build_message
    assert build_message(["ERROR", "web-01", "disk full"]) == "ERROR | web-01 | disk full"

def test_single_item():
    from broken import build_message
    assert build_message(["INFO"]) == "INFO"

def test_two_items():
    from broken import build_message
    assert build_message(["WARN", "high-cpu"]) == "WARN | high-cpu"
