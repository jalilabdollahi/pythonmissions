# Mission 011 - Regex Log Parser
# Fix the 2 bugs in this script.
import re

LOG_PATTERN = re.compile(
    r'(?P<ip>\d+\.\d+\.\d+\.\d+) - - \[(?P<timestamp>[^\]]+)\] '
    r'"(?P<method>\w+) (?P<path>[^ ]+) HTTP/[\d.]+" (?P<code>\d+) (?P<bytes>\d+)'
)

def parse_log_line(line):
    match = LOG_PATTERN.match(line)
    if not match:
        return None
    return {
        "ip": match.group("ip"),
        "timestamp": match.group("timestamp"),
        "method": match.group("method"),
        "path": match.group("path"),
        "status": int(match.group("status")),  # BUG 1: group name is "code" not "status"
        "bytes": int(match.group("bytes")),
    }

def get_error_rate(lines):
    parsed = [parse_log_line(l) for l in lines]
    parsed = [p for p in parsed if p]
    errors = [p for p in parsed if p["status"] => 400]  # BUG 2: invalid operator
    return len(errors) / len(parsed) if parsed else 0.0
