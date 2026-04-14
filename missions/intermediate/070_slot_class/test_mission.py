import pytest, sys
sys.path.insert(0, ".")
from broken import Metric

def test_create():
    m = Metric("cpu_usage", 75.5, 1700000000)
    assert m.name == "cpu_usage"
    assert m.value == 75.5
    assert m.timestamp == 1700000000

def test_tags():
    m = Metric("mem", 80, 1700000001, {"host": "web-01"})
    assert m.tags["host"] == "web-01"

def test_to_dict():
    m = Metric("disk", 90, 1700000002)
    d = m.to_dict()
    assert d["name"] == "disk"
