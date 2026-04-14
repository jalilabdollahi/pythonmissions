import pytest
import sys
sys.path.insert(0, ".")
from broken import percentile, summarize_latencies

DATA = [1, 5, 3, 9, 7, 2, 8, 4, 6, 10]  # sorted: 1..10

def test_percentile_50():
    result = percentile(DATA, 50)
    assert result == 5  # median of sorted [1..10] at index 5

def test_percentile_90():
    result = percentile(DATA, 90)
    assert result == 9

def test_summarize_count():
    s = summarize_latencies([10, 20, 30])
    assert s["count"] == 3
