import pytest, sys
sys.path.insert(0, ".")
from broken import PluginManager, BasePlugin

def test_setup_called():
    pm = PluginManager()
    p = BasePlugin("v1")
    pm.register("auth", p)
    assert p.setup_called is True

def test_teardown_on_swap():
    pm = PluginManager()
    old = BasePlugin("v1")
    new = BasePlugin("v2")
    pm.register("auth", old)
    pm.hot_swap("auth", new)
    assert old.teardown_called is True
    assert new.setup_called is True

def test_rollback():
    pm = PluginManager()
    old = BasePlugin("v1")
    new = BasePlugin("v2")
    pm.register("auth", old)
    pm.hot_swap("auth", new)
    pm.rollback("auth")
    assert pm.get("auth").name == "v1"
