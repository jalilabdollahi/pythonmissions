import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

from broken import Field, IntRange, Model, OneOf, Text, WorkerPool


def test_valid_values_are_stored_and_defaults_apply():
    pool = WorkerPool(name="  ingest  ", size=8)
    assert pool.name == "ingest", "text is stripped"
    assert pool.size == 8
    assert pool.mode == "thread" and pool.retries == 3


def test_each_instance_keeps_its_own_values():
    a = WorkerPool(name="a", size=2)
    b = WorkerPool(name="b", size=32)
    assert (a.name, a.size) == ("a", 2), "values belong to the instance, not to the descriptor"
    assert (b.name, b.size) == ("b", 32)
    a.mode = "process"
    assert b.mode == "thread"


def test_two_fields_on_one_class_do_not_collide():
    class Window(Model):
        low = IntRange(0, 100)
        high = IntRange(0, 100)

    w = Window(low=10, high=90)
    assert (w.low, w.high) == (10, 90), "__set_name__ must give every field its own storage key"


def test_the_same_descriptor_type_in_a_subclass_is_independent():
    class Big(WorkerPool):
        size = IntRange(1, 1024, default=128)

    assert Big().size == 128 and WorkerPool().size == 4
    assert Big(name="x", size=500).size == 500
    with pytest.raises(ValueError):
        WorkerPool(name="x", size=500)


def test_invalid_assignment_is_rejected_and_keeps_the_old_value():
    pool = WorkerPool(name="ok", size=5)
    with pytest.raises(ValueError, match="size must be between 1 and 64"):
        pool.size = 65
    with pytest.raises(TypeError):
        pool.size = "7"
    with pytest.raises(ValueError, match="one of"):
        pool.mode = "fiber"
    assert pool.size == 5 and pool.mode == "thread"


def test_booleans_are_not_accepted_as_integers():
    pool = WorkerPool(name="ok")
    with pytest.raises(TypeError):
        pool.size = True
    with pytest.raises(TypeError):
        pool.retries = False


def test_required_fields_raise_until_set_and_can_be_deleted():
    pool = WorkerPool()
    with pytest.raises(AttributeError, match="name has not been set"):
        pool.name
    pool.name = "later"
    assert pool.name == "later"
    del pool.name
    with pytest.raises(AttributeError):
        pool.name
    with pytest.raises(ValueError):
        pool.name = "   "
    with pytest.raises(ValueError):
        pool.name = "x" * 33


def test_class_access_returns_the_descriptor_and_fields_are_discoverable():
    assert isinstance(WorkerPool.size, IntRange), "accessing a descriptor on the class returns the descriptor"
    assert WorkerPool.size.public == "size"
    assert list(WorkerPool.fields()) == ["name", "size", "mode", "retries"]
    assert WorkerPool(name="n", retries=0).as_dict() == {"name": "n", "size": 4, "mode": "thread", "retries": 0}
    with pytest.raises(TypeError):
        WorkerPool(name="n", colour="red")
