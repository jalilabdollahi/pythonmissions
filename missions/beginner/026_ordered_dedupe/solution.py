# Mission 026 - Blocklist Out of Order (solution)
# Turn raw access-log lines into an ordered firewall blocklist.


def unique_offenders(log_lines):
    ips = [line.split()[0] for line in log_lines if line.strip()]
    return list(dict.fromkeys(ips))


def build_blocklist(log_lines, limit):
    offenders = unique_offenders(log_lines)
    return offenders[:limit]


if __name__ == "__main__":
    sample = ["10.0.0.9 - GET /admin", "10.0.0.2 - GET /admin", "10.0.0.9 - GET /login"]
    print(build_blocklist(sample, 5))
