import pytest
import sys
sys.path.insert(0, ".")
from broken import CircularBuffer

def test_write_and_read():
    b = CircularBuffer(3)
    b.write("a")
    b.write("b")
    assert b.read_all() == ["a", "b"]

def test_wrap_around():
    b = CircularBuffer(3)
    for i in range(5):
        b.write(str(i))
    result = b.read_all()
    assert len(result) == 3
    assert "4" in result

def test_is_full():
    b = CircularBuffer(2)
    b.write("x")
    assert not b.is_full()
    b.write("y")
    assert b.is_full()
