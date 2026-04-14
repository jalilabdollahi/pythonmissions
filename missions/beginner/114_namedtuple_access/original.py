# Mission 114 - Access the Server Record
from collections import namedtuple

Server = namedtuple("Server", ["name", "host", "port"])

def get_port(server):
    """Return the port number from a Server namedtuple."""
    return server[0]

if __name__ == "__main__":
    s = Server("web-01", "localhost", 8080)
    print(get_port(s))
