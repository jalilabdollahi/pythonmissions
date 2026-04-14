import os, sys
sys.path.insert(0, os.path.dirname(__file__))

def test_prints_correct_count(capsys):
    from broken import countdown
    countdown(3)
    out = capsys.readouterr().out.strip().split("\n")
    assert out == ["3", "2", "1"]

def test_zero_no_output(capsys):
    from broken import countdown
    countdown(0)
    assert capsys.readouterr().out == ""

def test_returns_none():
    from broken import countdown
    assert countdown(1) is None
