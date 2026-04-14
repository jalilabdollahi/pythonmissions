import pytest, sys
sys.path.insert(0, ".")
from broken import GCounter

def test_increment():
    g = GCounter("n1")
    g.increment(5)
    assert g.value() == 5

def test_merge_independent():
    g1 = GCounter("n1"); g1.increment(3)
    g2 = GCounter("n2"); g2.increment(7)
    merged = g1.merge(g2)
    assert merged.value() == 10

def test_merge_idempotent():
    g1 = GCounter("n1"); g1.increment(5)
    merged1 = g1.merge(g1)
    merged2 = merged1.merge(g1)
    assert merged2.value() == 5  # idempotent: same data merged twice stays 5
