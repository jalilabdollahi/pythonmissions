# Mission 114 - Solution
from collections import namedtuple

Server = namedtuple("Server", ["name", "host", "port"])

def get_port(server):
    return server.port

if __name__ == "__main__":
    s = Server("web-01", "localhost", 8080)
    print(get_port(s))
