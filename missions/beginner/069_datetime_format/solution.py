# Mission 069 - Solution
from datetime import datetime

def format_timestamp(dt):
    return dt.strftime("%Y-%m-%d %H:%M:%S")

if __name__ == "__main__":
    dt = datetime(2024, 3, 15, 14, 30, 0)
    print(format_timestamp(dt))
