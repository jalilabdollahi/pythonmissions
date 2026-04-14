import pytest, sys
sys.path.insert(0, ".")
from broken import process_batch, sum_squares

def test_process_batch():
    result = process_batch([1, 2, 3, 4])
    assert result == [1, 4, 9, 16]

def test_sum_squares():
    assert sum_squares([1, 2, 3]) == 14
