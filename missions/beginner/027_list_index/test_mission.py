import os, sys
sys.path.insert(0, os.path.dirname(__file__))

def test_found():
    from broken import get_node_index
    assert get_node_index(["node-01", "node-02", "node-03"], "node-02") == 1

def test_not_found():
    from broken import get_node_index
    assert get_node_index(["node-01", "node-02"], "node-99") == -1

def test_first_element():
    from broken import get_node_index
    assert get_node_index(["node-01", "node-02"], "node-01") == 0

def test_empty_list():
    from broken import get_node_index
    assert get_node_index([], "node-01") == -1
