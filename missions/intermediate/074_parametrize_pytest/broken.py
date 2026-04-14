# Mission 074 - Parametrize Pytest
# Fix the 2 bugs in this script.

def validate_port(port):
    """Return True if port is valid (1-65535)."""
    if not isinstance(port, int):
        return False
    return 1 <= port <= 65535

def classify_port(port):
    if port < 1024:
        return "system"
    elif port < 49152:
        return "registered"
    else:
        return "dynamic"
