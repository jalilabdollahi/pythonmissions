# Mission 021 - Dataclass Service Config
# Fix the 2 bugs in this script.
from dataclasses import dataclass, field

@dataclass
class ServiceConfig:
    host: str = "localhost"  # BUG 1: field with default before field without default
    port: int
    debug: bool = False
    tags: list = field(default_factory=list)

    def __post_init_hook__(self):  # BUG 2: should be __post_init__
        if self.port < 1 or self.port > 65535:
            raise ValueError(f"Invalid port: {self.port}")
        if not self.host:
            raise ValueError("Host cannot be empty")
