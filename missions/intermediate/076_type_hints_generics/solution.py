# Mission 076 - Type Hints Generics
# Fixed solution
from typing import TypeVar, Generic, Optional, Dict

K = TypeVar("K")
V = TypeVar("V")

class TypedCache(Generic[K, V]):
    def __init__(self):
        self._store: Dict[K, V] = {}

    def set(self, key: K, value: V) -> None:
        self._store[key] = value

    def get(self, key: K) -> Optional[V]:
        return self._store.get(key)

    def keys(self) -> list:
        return list(self._store.keys())
