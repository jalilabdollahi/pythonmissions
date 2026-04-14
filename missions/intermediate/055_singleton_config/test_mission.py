import pytest, sys
sys.path.insert(0, ".")
from broken import ConfigManager

def test_singleton():
    a = ConfigManager()
    b = ConfigManager()
    assert a is b

def test_shared_state():
    a = ConfigManager()
    a.set("env", "prod")
    b = ConfigManager()
    assert b.get("env") == "prod"
