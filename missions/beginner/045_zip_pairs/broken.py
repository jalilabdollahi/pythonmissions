# Mission 045 - Pair the Hosts and Ports
# Fix the bug.

def pair_services(hosts, ports):
    """Return list of (host, port) tuples."""
    return list(zip(hosts, ports))

if __name__ == "__main__":
    hosts = ["web-01", "api-01", "db-01"]
    ports = [80, 8080]
    print(pair_services(hosts, ports))
