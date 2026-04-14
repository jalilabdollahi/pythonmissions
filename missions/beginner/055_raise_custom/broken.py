# Mission 055 - Raise a Custom Error
def validate_port(port):
    """Raise ValueError if port is not in 1-65535 range."""
    if not (1 <= port <= 65535):
        raise Exception(f"Invalid port: {port}")
    return port

if __name__ == "__main__":
    try:
        validate_port(99999)
    except ValueError as e:
        print(f"Caught: {e}")
