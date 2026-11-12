# Mission 029 - IPv6 Replica Endpoints (solution)
# Parse "host:port" replica entries, including bracketed IPv6.


def parse_endpoint(text, default_port=5432):
    text = text.strip()
    if ":" not in text:
        return text, default_port
    host, port = text.rsplit(":", 1)
    host = host.strip("[]")
    return host, int(port)


def replica_map(entries):
    result = {}
    for entry in entries:
        host, port = parse_endpoint(entry)
        result[host] = port
    return result
