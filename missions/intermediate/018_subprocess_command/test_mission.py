import pytest
import sys
sys.path.insert(0, ".")
from broken import run_command

def test_run_success():
    out, code = run_command("echo hello")
    assert "hello" in out
    assert code == 0

def test_run_failure():
    with pytest.raises(RuntimeError):
        run_command("exit 2")
