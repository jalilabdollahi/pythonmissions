import os, sys, tempfile
from pathlib import Path
sys.path.insert(0, os.path.dirname(__file__))

def test_finds_yaml():
    from broken import find_yaml_files
    d = tempfile.mkdtemp()
    Path(d, "config.yaml").write_text("host: localhost")
    Path(d, "deploy.yaml").write_text("env: prod")
    result = find_yaml_files(d)
    assert len(result) == 2

def test_no_other_files():
    from broken import find_yaml_files
    d = tempfile.mkdtemp()
    Path(d, "readme.txt").write_text("hello")
    assert find_yaml_files(d) == []
