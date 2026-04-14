import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from datetime import datetime

def test_six_hours():
    from broken import uptime_hours
    start = datetime(2024, 3, 15, 0, 0, 0)
    end = datetime(2024, 3, 15, 6, 0, 0)
    assert uptime_hours(start, end) == 6.0

def test_half_hour():
    from broken import uptime_hours
    start = datetime(2024, 3, 15, 0, 0, 0)
    end = datetime(2024, 3, 15, 0, 30, 0)
    assert uptime_hours(start, end) == 0.5
