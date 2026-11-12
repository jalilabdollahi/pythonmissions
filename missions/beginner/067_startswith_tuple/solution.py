# Mission 067 - Only The First Prefix Counts (solution)
# Classifies destination addresses for the egress audit.

INTERNAL_PREFIXES = ("10.", "192.168.", "172.16.")


def is_internal(ip):
    return ip.startswith(INTERNAL_PREFIXES)


def external_only(ips):
    return [ip for ip in ips if not is_internal(ip)]


def internal_only(ips):
    return [ip for ip in ips if is_internal(ip)]


def summary(ips):
    inside = len(internal_only(ips))
    outside = len(external_only(ips))
    return "%d internal, %d external" % (inside, outside)


def is_loopback(ip):
    return ip.startswith("127.")


def audit_lines(ips):
    lines = []
    for ip in ips:
        label = "internal" if is_internal(ip) else "EXTERNAL"
        lines.append("%s %s" % (ip, label))
    return lines


if __name__ == "__main__":
    print(summary(["10.0.0.1", "8.8.8.8", "192.168.1.1"]))
