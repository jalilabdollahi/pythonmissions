import os, sys
sys.path.insert(0, os.path.dirname(__file__))

def test_max_100():
    from broken import LogWindow
    w = LogWindow()
    for i in range(150):
        w.add(f"line {i}")
    assert len(w.lines()) == 100

def test_keeps_latest():
    from broken import LogWindow
    w = LogWindow()
    for i in range(150):
        w.add(f"line {i}")
    assert "line 149" in w.lines()
    assert "line 0" not in w.lines()
