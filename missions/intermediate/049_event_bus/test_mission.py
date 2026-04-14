import pytest
import sys
sys.path.insert(0, ".")
from broken import EventBus

def test_subscribe_and_publish():
    bus = EventBus()
    received = []
    bus.subscribe("deploy", lambda d: received.append(d))
    bus.publish("deploy", {"version": "v2"})
    assert len(received) == 1
    assert received[0]["version"] == "v2"

def test_unsubscribe():
    bus = EventBus()
    received = []
    handler = lambda d: received.append(d)
    bus.subscribe("deploy", handler)
    bus.subscribe("deploy", lambda d: None)  # keep one subscriber
    bus.unsubscribe("deploy", handler)
    bus.publish("deploy", {})
    assert len(received) == 0

def test_unknown_event():
    bus = EventBus()
    count = bus.publish("unknown_event")
    assert count == 0
