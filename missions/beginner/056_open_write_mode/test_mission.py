import os, sys, tempfile
sys.path.insert(0, os.path.dirname(__file__))

def test_writes_message():
    from broken import write_log
    with tempfile.NamedTemporaryFile(delete=False, suffix='.log') as f:
        name = f.name
    write_log(name, "Deploy started")
    assert "Deploy started" in open(name).read()

def test_appends():
    from broken import write_log
    with tempfile.NamedTemporaryFile(delete=False, suffix='.log') as f:
        name = f.name
    write_log(name, "line1")
    write_log(name, "line2")
    content = open(name).read()
    assert "line1" in content and "line2" in content
