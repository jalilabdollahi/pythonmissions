# Mission 021 (Advanced) - Type-Safe Config Builder
# Fixed solution
from typing import TypeVar, Generic, Protocol, runtime_checkable

@runtime_checkable
class Validatable(Protocol):
    def validate(self) -> bool: ...
    def to_dict(self) -> dict: ...

T = TypeVar("T", bound=object)

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
