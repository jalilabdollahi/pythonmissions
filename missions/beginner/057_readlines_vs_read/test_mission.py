import os, sys, tempfile
sys.path.insert(0, os.path.dirname(__file__))

def make_file(content):
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.log') as f:
        f.write(content)
        return f.name

def test_returns_list():
    from broken import read_lines
    name = make_file("line1\nline2\n")
    assert isinstance(read_lines(name), list)

def test_correct_lines():
    from broken import read_lines
    name = make_file("line1\nline2\nline3\n")
    assert read_lines(name) == ["line1", "line2", "line3"]

def test_skips_empty():
    from broken import read_lines
    name = make_file("line1\n\nline3\n")
    assert "" not in read_lines(name)
