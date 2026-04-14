# Mission 070 - Solution
from datetime import datetime

def parse_log_time(s):
    return datetime.strptime(s, "%Y-%m-%d %H:%M:%S")

if __name__ == "__main__":
    print(parse_log_time("2024-03-15 14:30:00"))
