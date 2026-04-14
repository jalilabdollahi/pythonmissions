# Mission 076 - Type Hints Generics
# Fix the 2 bugs in this script.
from typing import TypeVar, Generic, Optional, Dict

K = TypeVar("K")
V = TypeVar("V")

class TypedCache(Generic[K, V]):
    def __init__(self):
        self._store: dict = {}  # BUG 1: should be Dict[K, V]

    def set(self, key: K, value: V) -> None:
        self._store[key] = value

    def get(self, key: K) -> Optional[str]:  # BUG 2: return type should be Optional[V]
        return self._store.get(key)

    def keys(self) -> list:
        return list(self._store.keys())
