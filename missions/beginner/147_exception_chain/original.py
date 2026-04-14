# Mission 147 - Chain the DB Exception
class ServiceError(Exception):
    pass

def connect(host):
    """Connect to host, raising ServiceError on failure."""
    try:
        raise ConnectionRefusedError(f"Connection refused by {host}")
    except ConnectionRefusedError as e:
        raise ServiceError(f"Cannot connect to {host}")

if __name__ == "__main__":
    try:
        connect("db.internal")
    except ServiceError as e:
        print(f"Error: {e}")
        print(f"Cause: {e.__cause__}")
