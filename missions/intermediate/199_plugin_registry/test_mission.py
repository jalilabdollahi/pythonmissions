import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import broken


@pytest.fixture(autouse=True)
def fresh_registry():
    saved = dict(broken._REGISTRY)
    yield
    broken.clear_registry()
    broken._REGISTRY.update(saved)


def test_decorated_class_is_still_the_class():
    @broken.register("memory")
    class MemorySink:
        pass

    assert MemorySink is not None, "the decorator must return the class it decorated"
    assert isinstance(MemorySink(), MemorySink)


def test_builtin_sinks_stay_usable():
    assert broken.StdoutSink is not None
    assert broken.WebhookSink("http://x").url == "http://x"


def test_create_returns_an_instance_with_options():
    sink = broken.create("stdout", prefix="[ops] ")
    assert isinstance(sink, broken.StdoutSink)
    sink.emit("hi")
    assert sink.lines == ["[ops] hi"]


def test_each_create_call_gives_a_new_object():
    assert broken.create("webhook") is not broken.create("webhook")


def test_duplicate_registration_is_rejected():
    with pytest.raises(ValueError, match="webhook"):
        @broken.register("webhook")
        class Impostor:
            pass

    assert broken.create("webhook").__class__ is broken.WebhookSink, "original sink must survive"


def test_unknown_name_lists_known_sinks():
    with pytest.raises(KeyError) as info:
        broken.create("pager")
    assert "stdout" in str(info.value) and "webhook" in str(info.value)
