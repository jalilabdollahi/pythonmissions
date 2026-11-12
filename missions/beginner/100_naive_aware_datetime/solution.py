# Mission 100 - Naive Meets Aware (solution)
# Finds expired API tokens using timezone-aware UTC datetimes.
from datetime import datetime, timezone

FORMAT = "%Y-%m-%dT%H:%M:%S"


def utc_now():
    return datetime.now(timezone.utc)


def parse_expiry(text):
    return datetime.strptime(text, FORMAT).replace(tzinfo=timezone.utc)


def is_expired(token, now):
    return parse_expiry(token["expires"]) <= now


def expired_ids(tokens, now):
    return sorted(t["id"] for t in tokens if is_expired(t, now))


def seconds_to_expiry(token, now):
    return int((parse_expiry(token["expires"]) - now).total_seconds())


if __name__ == "__main__":
    sample = [{"id": "t1", "expires": "2020-01-01T00:00:00"}]
    print(expired_ids(sample, utc_now()))
