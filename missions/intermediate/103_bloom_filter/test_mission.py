import pytest, sys
sys.path.insert(0, ".")
from broken import BloomFilter

def test_add_and_check():
    bf = BloomFilter()
    bf.add("user:alice")
    assert bf.might_contain("user:alice") is True

def test_not_added():
    bf = BloomFilter()
    bf.add("user:alice")
    assert bf.might_contain("user:bob") is False

def test_multiple_items():
    bf = BloomFilter()
    for i in range(100):
        bf.add(f"key:{i}")
    for i in range(100):
        assert bf.might_contain(f"key:{i}") is True
