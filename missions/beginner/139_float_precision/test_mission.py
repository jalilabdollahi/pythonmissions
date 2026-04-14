import os, sys
sys.path.insert(0, os.path.dirname(__file__))

def test_rounds_to_2():
    from broken import round_metric
    assert round_metric(45.6789) == 45.68

def test_rounds_to_1():
    from broken import round_metric
    assert round_metric(99.9999, 1) == 100.0

def test_integer_input():
    from broken import round_metric
    assert round_metric(42, 2) == 42
