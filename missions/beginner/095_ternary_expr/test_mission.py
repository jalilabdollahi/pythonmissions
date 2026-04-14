import os, sys
sys.path.insert(0, os.path.dirname(__file__))

def test_200():
    from broken import classify
    assert classify(200) == "ok"

def test_404():
    from broken import classify
    assert classify(404) == "error"

def test_500():
    from broken import classify
    assert classify(500) == "error"

def test_302():
    from broken import classify
    assert classify(302) == "ok"

def test_batch():
    from broken import batch_classify
    assert batch_classify([200, 500]) == ["ok", "error"]
