# Mission 011 - Find the Service Port
# Fix the bug.

def find_port_offset(line):
    """Return position of 'port' in line, or -1 if not found."""
    return line.index("port")

if __name__ == "__main__":
    print(find_port_offset("service port=8080"))
    print(find_port_offset("service name=web"))
