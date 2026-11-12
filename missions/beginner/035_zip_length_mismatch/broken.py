# Mission 035 - Silent Zip Truncation
# Pair migrated hostnames with their new IP addresses.


def pair_hosts(hostnames, addresses):
    return dict(zip(hostnames, addresses))


def render_zone(mapping):
    return [f"{host} IN A {ip}" for host, ip in sorted(mapping.items())]


if __name__ == "__main__":
    pairs = pair_hosts(["app1", "app2"], ["10.1.0.4", "10.1.0.5"])
    print("\n".join(render_zone(pairs)))
