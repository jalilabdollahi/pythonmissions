# Mission 071 - Solution
from datetime import datetime

def uptime_hours(start, end):
    delta = end - start
    return delta.total_seconds() / 3600

if __name__ == "__main__":
    from datetime import datetime
    start = datetime(2024, 3, 15, 0, 0, 0)
    end = datetime(2024, 3, 15, 6, 0, 0)
    print(uptime_hours(start, end))
