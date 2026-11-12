# Mission 112 - Log Line Spotter
# Finds error lines and request IDs inside timestamped log lines.
import re

ERROR_WORD = re.compile(r"\bERROR\b")
REQUEST_ID = re.compile(r"req-(\d+)")


def has_error(line):
    return ERROR_WORD.match(line) is not None


def request_id(line):
    found = REQUEST_ID.match(line)
    if found is None:
        return None
    return int(found.group(1))


def count_errors(lines):
    return sum(1 for line in lines if has_error(line))


def error_ids(lines):
    ids = []
    for line in lines:
        if has_error(line):
            ids.append(request_id(line))
    return ids


if __name__ == "__main__":
    sample = ["2025-03-01T10:00:00 ERROR db timeout req-4821", "2025-03-01T10:00:01 INFO ok"]
    print(count_errors(sample), error_ids(sample))
