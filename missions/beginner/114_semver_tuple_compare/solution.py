# Mission 114 - Release Gatekeeper (solution)
# Compares dotted version numbers to decide which release is newer.
def parse_version(text):
    return tuple(int(part) for part in text.strip().split("."))


def is_newer(a, b):
    return parse_version(a) > parse_version(b)


def latest_release(versions):
    return max(versions, key=parse_version)


def needs_upgrade(current, minimum):
    return is_newer(minimum, current)


def hosts_to_upgrade(fleet, minimum):
    # fleet maps hostname -> installed agent version
    return sorted(host for host, version in fleet.items() if needs_upgrade(version, minimum))


if __name__ == "__main__":
    fleet = {"web-1": "1.9.0", "web-2": "1.10.0", "db-1": "1.2.3"}
    print(hosts_to_upgrade(fleet, "1.10.0"))
