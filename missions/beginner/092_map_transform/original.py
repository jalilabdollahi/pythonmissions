# Mission 092 - Convert Ports to Integers
def int_ports(port_strings):
    """Convert list of port strings to list of ints."""
    return map(int, port_strings)

if __name__ == "__main__":
    ports = ["80", "443", "8080", "5432"]
    result = int_ports(ports)
    print(type(result), result)
