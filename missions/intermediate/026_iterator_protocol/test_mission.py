import pytest
import sys
sys.path.insert(0, ".")
from broken import LogIterator

LOGS = ["INFO start", "ERROR crash", "INFO done"]

def test_iterate_all():
    it = LogIterator(LOGS)
    result = list(it)
    assert result == LOGS

def test_for_loop():
    count = 0
    for entry in LogIterator(LOGS):
        count += 1
    assert count == 3

def test_empty():
    it = LogIterator([])
    assert list(it) == []
