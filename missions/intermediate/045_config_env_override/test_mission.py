import pytest
import sys
import os
sys.path.insert(0, ".")
from broken import load_with_env_override, get_workers, DEFAULTS

def test_defaults():
    os.environ.pop("PORT", None)
    cfg = load_with_env_override()
    assert cfg["PORT"] == 8080

def test_env_override():
    os.environ["PORT"] = "9000"
    cfg = load_with_env_override()
    assert cfg["PORT"] == 9000
    assert isinstance(cfg["PORT"], int)
    del os.environ["PORT"]

def test_get_workers():
    os.environ.pop("WORKERS", None)
    result = get_workers()
    assert result == 5
