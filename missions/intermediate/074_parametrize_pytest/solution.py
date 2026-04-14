# Mission 074 - Parametrize Pytest
# Fixed solution

def validate_port(port):
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
