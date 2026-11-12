# Mission 211 - Maintenance Window Clock (solution)
# Convert local maintenance windows to UTC with zoneinfo, including DST days.
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

STANDARD_OFFSETS = {"Europe/Berlin": 1, "America/New_York": -5}


def window_to_utc(day, start, duration_minutes, tz_name):
    naive = datetime.strptime(f"{day} {start}", "%Y-%m-%d %H:%M")
    local = naive.replace(tzinfo=ZoneInfo(tz_name))
    start_utc = local.astimezone(timezone.utc)
    end_utc = start_utc + timedelta(minutes=duration_minutes)
    return start_utc, end_utc


def local_label(utc_dt, tz_name):
    local = utc_dt.astimezone(ZoneInfo(tz_name))
    return local.strftime("%Y-%m-%d %H:%M %Z")


def windows_overlap(a, b):
    return a[0] < b[1] and b[0] < a[1]


def daily_windows(first_day, start, duration_minutes, tz_name, days):
    first = datetime.strptime(first_day, "%Y-%m-%d")
    windows = []
    for offset in range(days):
        day = (first + timedelta(days=offset)).strftime("%Y-%m-%d")
        windows.append(window_to_utc(day, start, duration_minutes, tz_name))
    return windows


def to_iso_z(dt):
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def announce(day, start, duration_minutes, tz_name):
    start_utc, end_utc = window_to_utc(day, start, duration_minutes, tz_name)
    return f"{local_label(start_utc, tz_name)} -> {local_label(end_utc, tz_name)}"


if __name__ == "__main__":
    print(announce("2024-03-31", "00:30", 240, "Europe/Berlin"))
