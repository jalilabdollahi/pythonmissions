import pytest, sys
sys.path.insert(0, ".")
from broken import calculate_sla, incident_duration
from datetime import datetime, timedelta

START = datetime(2024, 1, 1, 0, 0, 0)
END = datetime(2024, 1, 1, 1, 0, 0)  # 1 hour period

def test_no_incidents():
    assert calculate_sla([], START, END) == 100.0

def test_with_incident():
    inc = {"start": datetime(2024, 1, 1, 0, 30), "end": datetime(2024, 1, 1, 0, 36)}
    sla = calculate_sla([inc], START, END)
    assert sla == 99.0  # 6 min downtime in 60 min = 90% down? No: 6/60=10% down, 90% up

def test_incident_duration():
    s = datetime(2024, 1, 1, 0, 0)
    e = datetime(2024, 1, 1, 0, 5)
    assert incident_duration(s, e) == 300.0
