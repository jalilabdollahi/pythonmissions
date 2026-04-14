# Mission 021 (Advanced) - Type-Safe Config Builder
# Fix the 2 bugs in this script.
from typing import TypeVar, Generic, Protocol, runtime_checkable

@runtime_checkable
class Validatable:  # BUG 1: should inherit from Protocol
    def validate(self) -> bool: ...
    def to_dict(self) -> dict: ...

T = TypeVar("T", Validatable, dict)  # BUG 2: should use bound= not positional constraint

class ConfigBuilder(Generic[T]):
    def __init__(self, config_type: type):
        self._config_type = config_type
        self._values = {}

    def set(self, key: str, value) -> "ConfigBuilder[T]":
        self._values[key] = value
        return self

    def build(self) -> T:
        obj = self._config_type(**self._values)
        if isinstance(obj, Validatable):
            if not obj.validate():
                raise ValueError("Config validation failed")
        return obj
