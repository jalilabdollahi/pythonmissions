import pytest, sys
sys.path.insert(0, ".")
from broken import Trie

def test_insert_search():
    t = Trie()
    t.insert("deploy")
    assert t.search("deploy") is True

def test_prefix_not_word():
    t = Trie()
    t.insert("deploy")
    assert t.search("depl") is False
    assert t.starts_with("depl") is True

def test_not_found():
    t = Trie()
    t.insert("rollback")
    assert t.search("scale") is False
