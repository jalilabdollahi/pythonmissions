import os, sys, types
sys.path.insert(0, os.path.dirname(__file__))

def test_returns_generator():
    from broken import metric_lines
    result = metric_lines({"cpu": 45})
    assert hasattr(result, "__next__")

def test_yields_correct_lines():
    from broken import metric_lines
    result = list(metric_lines({"cpu": 45, "mem": 78}))
    assert "cpu=45" in result
    assert "mem=78" in result
