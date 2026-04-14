# Mission 105 - Split Host from Port
def split_host_port(endpoint):
    """Return (host, port) from 'host:port' or 'ipv6:port'."""
    parts = endpoint.split(":")
    return parts[0], parts[-1]

if __name__ == "__main__":
    print(split_host_port("localhost:8080"))
    print(split_host_port("::1:8080"))
