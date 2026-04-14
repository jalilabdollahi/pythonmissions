import os, sys
sys.path.insert(0, os.path.dirname(__file__))

def test_prints_percentage(capsys):
    from broken import print_progress
    print_progress(1, 4)
    out = capsys.readouterr().out
    assert "25%" in out

def test_prints_100(capsys):
    from broken import print_progress
    print_progress(5, 5)
    out = capsys.readouterr().out
    assert "100%" in out
