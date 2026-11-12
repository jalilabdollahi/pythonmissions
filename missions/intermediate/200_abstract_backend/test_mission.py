import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import broken


def test_base_class_cannot_be_instantiated():
    with pytest.raises(TypeError):
        broken.ArtifactStore()


def test_incomplete_subclass_fails_at_construction():
    class HalfStore(broken.ArtifactStore):
        def put(self, key, data):
            pass

    with pytest.raises(TypeError):
        HalfStore()


def test_directory_store_roundtrip_and_delete(tmp_path):
    store = broken.DirectoryStore(tmp_path / "artifacts")
    store.put("app.tar", b"123")
    assert store.get("app.tar") == b"123"
    assert store.exists("app.tar")
    store.delete("app.tar")
    assert store.get("app.tar") is None
    store.delete("app.tar")


def test_directory_store_default_value(tmp_path):
    assert broken.DirectoryStore(tmp_path).get("nope", b"fallback") == b"fallback"


def test_memory_store_roundtrip_and_delete():
    store = broken.MemoryStore()
    store.put("a", b"1")
    assert store.get("a") == b"1"
    store.delete("a")
    assert store.get("a") is None


def test_memory_store_accepts_default_like_the_interface():
    store = broken.MemoryStore()
    assert store.get("missing", b"x") == b"x", "same signature as ArtifactStore.get"


def test_exists_works_for_every_backend(tmp_path):
    for store in (broken.MemoryStore(), broken.DirectoryStore(tmp_path)):
        store.put("k", b"v")
        assert store.exists("k")
        assert not store.exists("other")
