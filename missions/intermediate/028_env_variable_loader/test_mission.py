import pytest
import sys
import os
sys.path.insert(0, ".")
from broken import load_env, get_port

def test_missing_key_returns_default():
    os.environ.pop("TEST_MISSING_KEY_XYZ", None)
    result = load_env("TEST_MISSING_KEY_XYZ", default="fallback")
    assert result == "fallback"

def test_cast_to_int():
    os.environ["TEST_PORT_XYZ"] = "9090"
    result = load_env("TEST_PORT_XYZ", cast=int)
    assert result == 9090
    assert isinstance(result, int)

def test_get_port_default():
    os.environ.pop("PORT", None)
    assert get_port() == 8080
