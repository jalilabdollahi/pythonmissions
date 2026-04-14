# Mission 123 - SLA Calculator
# Fix the 2 bugs in this script.
from datetime import datetime

def incident_duration(start, end):
    """Return duration in seconds."""
    return (start - end).total_seconds()  # BUG 1: should be end - start

def calculate_sla(incidents, period_start, period_end):
    """Calculate SLA uptime percentage for a period."""
    total_seconds = (period_end - period_start).total_seconds()
    if total_seconds <= 0:
        return 100.0
    downtime = 0
    for inc in incidents:
        s = max(inc["start"], period_start)
        e = min(inc["end"], period_end)
        if e > s:
            downtime += incident_duration(s, e)
    uptime_pct = (downtime / total_seconds) * 100  # BUG 2: should be (total - downtime) / total
    return round(uptime_pct, 4)
