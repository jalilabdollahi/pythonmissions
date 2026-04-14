import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from datetime import datetime

def test_parses_correctly():
    from broken import parse_log_time
    dt = parse_log_time("2024-03-15 14:30:00")
    assert dt == datetime(2024, 3, 15, 14, 30, 0)

def test_year():
    from broken import parse_log_time
    assert parse_log_time("2024-03-15 14:30:00").year == 2024

def test_month():
    from broken import parse_log_time
    assert parse_log_time("2024-03-15 14:30:00").month == 3
