# Mission 06 - Parse Nginx Logs
# Fix the 2 bugs in this script.

import re
from collections import Counter

LOG_PATTERN = r'(\d+\.\d+\.\d+\.\d+).*?"[A-Z]+ \S+ HTTP/\d\.\d" (\d{3})'


def find_5xx_ips(log_content):
    """Return list of IPs that received a 5xx response."""
    ips = []
    for line in log_content.strip().splitlines():
        if not line:
            continue
        match = re.match(LOG_PATTERN, line)
        if match:
            ip = match.group(1)
            status = match.group(3)
            if status.startswith("5"):
                ips.append(ip)
    return ips


def top_offenders(log_content, n=3):
    ips = find_5xx_ips(log_content)
    return Counter(ips).most_common(n)


if __name__ == "__main__":
    sample = """
10.0.0.1 - - [10/Jan/2024:10:00:01 +0000] "GET /api HTTP/1.1" 500 1234
10.0.0.2 - - [10/Jan/2024:10:00:02 +0000] "POST /login HTTP/1.1" 200 567
10.0.0.1 - - [10/Jan/2024:10:00:03 +0000] "GET /api HTTP/1.1" 502 890
10.0.0.3 - - [10/Jan/2024:10:00:04 +0000] "GET /health HTTP/1.1" 503 12
"""
    print("Top offenders:", top_offenders(sample))
