import pytest
import sys
sys.path.insert(0, ".")
from broken import LRUCache

def test_basic_get_put():
    c = LRUCache(2)
    c.put("a", 1)
    c.put("b", 2)
    assert c.get("a") == 1

def test_eviction():
    c = LRUCache(2)
    c.put("a", 1)
    c.put("b", 2)
    c.get("a")  # "a" becomes most recently used
    c.put("c", 3)  # "b" should be evicted (LRU)
    assert c.get("b") == -1
    assert c.get("a") == 1

def test_size():
    c = LRUCache(3)
    c.put("x", 10)
    c.put("y", 20)
    assert c.size() == 2
