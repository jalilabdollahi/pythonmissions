# Mission 147 - Solution
class ServiceError(Exception):
    pass

def connect(host):
    try:
        raise ConnectionRefusedError(f"Connection refused by {host}")
    except ConnectionRefusedError as e:
        raise ServiceError(f"Cannot connect to {host}") from e

if __name__ == "__main__":
    try:
        connect("db.internal")
    except ServiceError as e:
        print(f"Error: {e}")
        print(f"Cause: {e.__cause__}")
