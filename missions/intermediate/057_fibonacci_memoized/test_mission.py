import pytest, sys
sys.path.insert(0, ".")
from broken import fib

def test_base_cases():
    assert fib(0) == 0
    assert fib(1) == 1

def test_sequence():
    assert [fib(i) for i in range(8)] == [0, 1, 1, 2, 3, 5, 8, 13]

def test_negative():
    with pytest.raises(ValueError):
        fib(-1)
