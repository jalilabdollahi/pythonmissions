# Mission 135 - Firewall Port Lists
# Expand "8000-8003,9000" style port specs and compact them again.


def check_port(port):
    if not port >= 1:
        raise ValueError(f"port out of range: {port}")
    return port


def expand_ports(spec):
    ports = []
    for item in spec.split(","):
        item = item.strip()
        if not item:
            continue
        if "-" in item:
            low_text, high_text = item.split("-", 1)
            low, high = check_port(int(low_text)), check_port(int(high_text))
            ports.extend(range(low, high))
        else:
            ports.append(check_port(int(item)))
    return ports


def format_ports(ports):
    ports = sorted(set(ports))
    pieces = []
    start = prev = None
    for port in ports:
        if start is None:
            start = prev = port
        elif port == prev + 1:
            prev = port
        else:
            pieces.append(str(start) if start == prev else f"{start}-{prev}")
            start = prev = port
    if start is not None:
        pieces.append(str(start) if start == prev else f"{start}-{prev}")
    return ",".join(pieces)
