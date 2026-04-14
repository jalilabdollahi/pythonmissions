# Mission 038 - Build the Port Map
# Fix the bug.

def build_port_map(names, ports):
    """Return a dict mapping service name to port number."""
    return {(name, port) for name, port in zip(names, ports)}

if __name__ == "__main__":
    names = ["web", "api", "db"]
    ports = [80, 8080, 5432]
    print(build_port_map(names, ports))
