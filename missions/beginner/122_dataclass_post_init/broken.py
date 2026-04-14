# Mission 122 - Validate Port in Dataclass
from dataclasses import dataclass

@dataclass
class Service:
    name: str
    port: int

    def __post_init_check__(self):
        if not (1 <= self.port <= 65535):
            raise ValueError(f"Invalid port: {self.port}")

if __name__ == "__main__":
    try:
        svc = Service("web", 99999)
        print("No error raised!")
    except ValueError as e:
        print(f"Caught: {e}")
