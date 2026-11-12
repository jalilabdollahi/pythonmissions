# Mission 200 - Artifact Store Contract
# Pluggable artifact storage with an abstract interface and two backends.
from abc import ABC, abstractmethod
from pathlib import Path


class ArtifactStore:
    @abstractmethod
    def put(self, key, data):
        """Store bytes under key."""

    @abstractmethod
    def get(self, key, default=None):
        """Return the bytes stored under key, or default."""

    @abstractmethod
    def delete(self, key):
        """Remove key if present."""

    def exists(self, key):
        sentinel = object()
        return self.get(key, sentinel) is not sentinel


class DirectoryStore(ArtifactStore):
    def __init__(self, root):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    def put(self, key, data):
        (self.root / key).write_bytes(data)

    def get(self, key, default=None):
        path = self.root / key
        return path.read_bytes() if path.exists() else default


class MemoryStore(ArtifactStore):
    def __init__(self):
        self._blobs = {}

    def put(self, key, data):
        self._blobs[key] = data

    def get(self, key):
        return self._blobs.get(key)

    def delete(self, key):
        self._blobs.pop(key, None)
