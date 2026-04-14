import os, sys
sys.path.insert(0, os.path.dirname(__file__))

def test_centered():
    from broken import center_text
    result = center_text("DEPLOY", 60)
    assert len(result) == 60

def test_content_present():
    from broken import center_text
    assert "DEPLOY" in center_text("DEPLOY", 60)
