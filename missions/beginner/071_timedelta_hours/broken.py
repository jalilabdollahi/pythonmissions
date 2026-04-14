# Mission 071 - Calculate Uptime Hours
from datetime import datetime

def uptime_hours(start, end):
    """Return uptime in hours between start and end datetimes."""
    delta = end - start
    return delta.total_seconds()

if __name__ == "__main__":
    from datetime import datetime, timedelta
    start = datetime(2024, 3, 15, 0, 0, 0)
    end = datetime(2024, 3, 15, 6, 0, 0)
    print(uptime_hours(start, end))
