# Mission 121 - Solution
from dataclasses import dataclass, field

@dataclass
class Server:
    name: str
    host: str
    port: int
    tags: list = field(default_factory=list)

if __name__ == "__main__":
    s = Server("web-01", "localhost", 8080)
    print(s)
