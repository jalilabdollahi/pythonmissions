import os, sys, tempfile
sys.path.insert(0, os.path.dirname(__file__))

def test_writes_content():
    from broken import ConfigWriter
    with tempfile.NamedTemporaryFile(delete=False, suffix='.cfg') as tmp:
        name = tmp.name
    with ConfigWriter(name) as f:
        f.write("host=localhost\n")
    assert "host=localhost" in open(name).read()

def test_closes_file():
    from broken import ConfigWriter
    with tempfile.NamedTemporaryFile(delete=False, suffix='.cfg') as tmp:
        name = tmp.name
    cw = ConfigWriter(name)
    with cw as f:
        f.write("x")
    assert cw.f.closed
