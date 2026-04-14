import pytest
import sys
sys.path.insert(0, ".")
from broken import LogRotator

def test_write_and_check(tmp_path):
    log = str(tmp_path / "app.log")
    arc = str(tmp_path / "app.log.1")
    r = LogRotator(log, arc, max_bytes=10000)
    result = r.write("hello world")
    assert result is True

def test_rotation(tmp_path):
    log = str(tmp_path / "app.log")
    arc = str(tmp_path / "app.log.1")
    r = LogRotator(log, arc, max_bytes=10)
    with open(log, "w") as f:
        f.write("x" * 100)
    r.rotate()
    assert os.path.getsize(log) == 0
    assert os.path.exists(arc)
