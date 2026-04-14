import os, sys
sys.path.insert(0, os.path.dirname(__file__))

def test_left_justified():
    from broken import align_name
    result = align_name("web", 10)
    assert result.startswith("web")
    assert result.endswith(" ")

def test_correct_length():
    from broken import align_name
    assert len(align_name("web", 10)) == 10
