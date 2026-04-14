# Mission 069 - Format the Deploy Timestamp
from datetime import datetime

def format_timestamp(dt):
    """Return datetime formatted as 'YYYY-MM-DD HH:MM:SS'."""
    return dt.strftime("%Y-%d-%m %H:%M:%S")

if __name__ == "__main__":
    dt = datetime(2024, 3, 15, 14, 30, 0)
    print(format_timestamp(dt))
