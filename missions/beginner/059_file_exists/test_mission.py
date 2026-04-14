import os, sys, tempfile
sys.path.insert(0, os.path.dirname(__file__))

def test_existing_file():
    from broken import file_exists
    with tempfile.NamedTemporaryFile(delete=False) as f:
        name = f.name
    assert file_exists(name) is True

def test_missing_file():
    from broken import file_exists
    assert file_exists("/nonexistent/path/file.txt") is False
