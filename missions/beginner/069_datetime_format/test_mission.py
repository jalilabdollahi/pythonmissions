import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from datetime import datetime

def test_format():
    from broken import format_timestamp
    dt = datetime(2024, 3, 15, 14, 30, 0)
    assert format_timestamp(dt) == "2024-03-15 14:30:00"

def test_month_is_correct():
    from broken import format_timestamp
    dt = datetime(2024, 3, 15, 0, 0, 0)
    result = format_timestamp(dt)
    assert result.split("-")[1] == "03"

def test_day_is_correct():
    from broken import format_timestamp
    dt = datetime(2024, 3, 15, 0, 0, 0)
    result = format_timestamp(dt)
    assert result.split("-")[2].split(" ")[0] == "15"
