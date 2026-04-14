import pytest
import sys
sys.path.insert(0, ".")
from broken import run_pipeline, count_words

def test_pipeline_result():
    result = run_pipeline("  The Server Is Running  ")
    assert "the" not in result
    assert "server" in result

def test_count_words():
    # "the server is running" -> normalize -> tokenize -> remove stops -> ["server", "running"]
    count = count_words("  The Server Is Running  ")
    assert count == 2
