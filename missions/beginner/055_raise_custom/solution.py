# Mission 055 - Solution
def validate_port(port):
    if not (1 <= port <= 65535):
        raise ValueError(f"Invalid port: {port}")
    return port

if __name__ == "__main__":
    try:
        validate_port(99999)
    except ValueError as e:
        print(f"Caught: {e}")
