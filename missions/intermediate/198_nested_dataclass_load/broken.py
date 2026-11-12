# Mission 198 - Nested Config Loader
# Build nested dataclasses from plain dicts, tolerating unknown keys.
from dataclasses import dataclass, fields, is_dataclass
from typing import Optional, Union, get_args, get_origin


@dataclass
class DatabaseConfig:
    host: str
    port: int = 5432


@dataclass
class CacheConfig:
    url: str
    ttl: int = 60


@dataclass
class ServiceConfig:
    name: str
    database: DatabaseConfig
    cache: Optional[CacheConfig] = None
    replicas: int = 1


def _unwrap(tp):
    return tp


def load(cls, data):
    declared = {f.name: f for f in fields(cls)}
    kwargs = {}
    for key, value in data.items():
        field_type = _unwrap(declared[key].type)
        if is_dataclass(field_type) and isinstance(value, dict):
            value = field_type(**value)
        kwargs[key] = value
    return cls(**kwargs)


if __name__ == "__main__":
    print(load(ServiceConfig, {"name": "api", "database": {"host": "db1"}}))
