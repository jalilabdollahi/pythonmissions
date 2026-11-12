# Mission 212 - Epoch Time Translator (solution)
# Convert between epoch timestamps and ISO-8601 UTC strings.
from datetime import datetime, timezone

ISO_SECONDS = "%Y-%m-%dT%H:%M:%SZ"


def epoch_to_iso(ts):
    return datetime.fromtimestamp(ts, tz=timezone.utc).strftime(ISO_SECONDS)


def epoch_ms_to_iso(ms):
    dt = datetime.fromtimestamp(ms / 1000, tz=timezone.utc)
    return dt.strftime("%Y-%m-%dT%H:%M:%S") + f".{dt.microsecond // 1000:03d}Z"


def iso_to_epoch(text):
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    dt = datetime.fromisoformat(text)
    return int(dt.timestamp())


def seconds_between(start_iso, end_iso):
    return iso_to_epoch(end_iso) - iso_to_epoch(start_iso)


def hour_bucket(ts):
    return epoch_to_iso(ts - ts % 3600)


def age_label(now_ts, iso_text):
    seconds = now_ts - iso_to_epoch(iso_text)
    if seconds < 60:
        return f"{seconds}s ago"
    if seconds < 3600:
        return f"{seconds // 60}m ago"
    return f"{seconds // 3600}h ago"


def ticket_stamp(ts):
    return f"[{epoch_to_iso(ts)}]"


if __name__ == "__main__":
    print(epoch_to_iso(1714564800), iso_to_epoch("2024-05-01T12:00:00Z"))
