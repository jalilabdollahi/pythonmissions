# Mission 121 - Build the Server Dataclass
from dataclasses import dataclass

@dataclass
class Server:
    name: str
    host: str
    port: int
    tags: list = []

if __name__ == "__main__":
    s = Server("web-01", "localhost", 8080)
    print(s)
