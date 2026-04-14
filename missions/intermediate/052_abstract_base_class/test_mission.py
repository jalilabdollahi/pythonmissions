import pytest, sys
sys.path.insert(0, ".")
from broken import BasePlugin, ConcretePlugin

def test_concrete_works():
    p = ConcretePlugin()
    assert p.execute("hello") == "HELLO"
    assert p.name() == "concrete"

def test_abstract_cannot_instantiate():
    with pytest.raises(TypeError):
        BasePlugin()
