# Mission 098 - Reading Log Timestamps (solution)
# Parses timestamps from two log formats to build an outage timeline.
from datetime import datetime

APP_FORMAT = "%Y-%m-%d %H:%M:%S"
ACCESS_FORMAT = "%d/%b/%Y:%H:%M:%S"


def parse_app_ts(text):
    return datetime.strptime(text, APP_FORMAT)


def parse_access_ts(text):
    return datetime.strptime(text, ACCESS_FORMAT)


def outage_minutes(start_text, end_text):
    delta = parse_app_ts(end_text) - parse_app_ts(start_text)
    return int(delta.total_seconds() // 60)


def same_hour(a, b):
    return a.replace(minute=0, second=0, microsecond=0) == b.replace(
        minute=0, second=0, microsecond=0
    )


if __name__ == "__main__":
    print(outage_minutes("2024-03-05 14:07:09", "2024-03-05 15:30:09"))
    print(parse_access_ts("05/Mar/2024:14:07:09"))
