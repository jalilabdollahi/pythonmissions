# Mission 021 - Dataclass Service Config
# Fixed solution
from dataclasses import dataclass, field

@dataclass
class ServiceConfig:
    port: int
    host: str = "localhost"
    debug: bool = False
    tags: list = field(default_factory=list)

    def __post_init__(self):
        if self.port < 1 or self.port > 65535:
            raise ValueError(f"Invalid port: {self.port}")
        if not self.host:
            raise ValueError("Host cannot be empty")
