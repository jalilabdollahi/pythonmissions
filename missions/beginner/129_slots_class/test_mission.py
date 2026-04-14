import os, sys
sys.path.insert(0, os.path.dirname(__file__))

def test_node_id():
    from broken import Node
    n = Node("n-001", 42)
    assert n.node_id == "n-001"

def test_value():
    from broken import Node
    n = Node("n-001", 42)
    assert n.value == 42

def test_has_slots():
    from broken import Node
    assert hasattr(Node, "__slots__")
