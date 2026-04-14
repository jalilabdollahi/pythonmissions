# Mission 123 - SLA Calculator
# Fixed solution
from datetime import datetime

def incident_duration(start, end):
    return (end - start).total_seconds()

def calculate_sla(incidents, period_start, period_end):
    total_seconds = (period_end - period_start).total_seconds()
    if total_seconds <= 0:
        return 100.0
    downtime = 0
    for inc in incidents:
        s = max(inc["start"], period_start)
        e = min(inc["end"], period_end)
        if e > s:
            downtime += incident_duration(s, e)
    uptime_pct = ((total_seconds - downtime) / total_seconds) * 100
    return round(uptime_pct, 4)
