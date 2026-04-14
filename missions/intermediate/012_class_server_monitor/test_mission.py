import pytest
import sys
sys.path.insert(0, ".")
from broken import ServerMonitor

def test_report():
    m = ServerMonitor("web-01")
    m.record(50, 60)
    m.record(70, 80)
    r = m.report()
    assert "web-01" in r
    assert "60.0" in r

def test_average_cpu():
    m = ServerMonitor("db-01")
    m.record(40, 50)
    m.record(60, 70)
    assert m.average_cpu() == 50.0
