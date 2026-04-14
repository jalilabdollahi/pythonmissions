import os, sys, tempfile
from pathlib import Path
sys.path.insert(0, os.path.dirname(__file__))

def test_creates_dir():
    from broken import ensure_log_dir
    base = tempfile.mkdtemp()
    target = os.path.join(base, "a", "b", "logs")
    ensure_log_dir(target)
    assert os.path.exists(target)

def test_idempotent():
    from broken import ensure_log_dir
    base = tempfile.mkdtemp()
    target = os.path.join(base, "logs")
    ensure_log_dir(target)
    ensure_log_dir(target)  # should not raise
