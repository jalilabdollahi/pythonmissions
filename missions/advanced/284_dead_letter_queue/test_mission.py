import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import Broker, PermanentError


class UnknownTenant(PermanentError):
    pass


def test_healthy_messages_are_processed_once():
    broker = Broker()
    broker.publish("m1", "ok")
    broker.publish("m2", "ok")
    calls = []
    broker.run(calls.append)
    assert broker.processed == ["m1", "m2"]
    assert calls == ["ok", "ok"]
    assert broker.dead == []


def test_flaky_message_succeeds_within_budget():
    broker = Broker(max_attempts=3)
    broker.publish("m1", "flaky")
    state = {"n": 0}

    def handler(body):
        state["n"] += 1
        if state["n"] < 3:
            raise RuntimeError("timeout")

    broker.run(handler)
    assert broker.processed == ["m1"], "third attempt is still inside a budget of three"
    assert broker.dead == []


def test_message_is_parked_after_exactly_max_attempts():
    broker = Broker(max_attempts=3)
    broker.publish("m1", "bad")
    calls = []

    def handler(body):
        calls.append(body)
        raise RuntimeError("boom")

    broker.run(handler)
    assert len(calls) == 3, "max_attempts means three deliveries, not four"
    assert broker.dead[0]["reason"] == "retries_exhausted"
    assert broker.dead[0]["attempts"] == 3


def test_dead_letter_records_the_latest_error():
    broker = Broker(max_attempts=3)
    broker.publish("m1", "bad")
    state = {"n": 0}

    def handler(body):
        state["n"] += 1
        raise RuntimeError(f"failure #{state['n']}")

    broker.run(handler)
    assert broker.dead[0]["last_error"] == "failure #3"


def test_permanent_error_subclass_is_parked_immediately():
    broker = Broker(max_attempts=5)
    broker.publish("m1", "x")
    calls = []

    def handler(body):
        calls.append(body)
        raise UnknownTenant("tenant 77 does not exist")

    broker.run(handler)
    assert len(calls) == 1, "permanent errors must not be retried"
    assert broker.dead[0]["reason"] == "permanent"


def test_poison_message_does_not_block_the_queue():
    broker = Broker(max_attempts=3)
    broker.publish("m1", "bad")
    broker.publish("m2", "good")
    seen = []

    def handler(body):
        seen.append(body)
        if body == "bad":
            raise RuntimeError("boom")

    broker.run(handler)
    assert seen == ["bad", "good", "bad", "bad"], "retries go to the back of the line"
    assert broker.processed == ["m2"]


def test_redrive_gives_a_fresh_budget():
    broker = Broker(max_attempts=2)
    broker.publish("m1", "bad")
    broker.run(lambda body: (_ for _ in ()).throw(RuntimeError("x")))
    assert broker.summary() == {"processed": 0, "dead": 1, "queued": 0}
    assert broker.redrive() == 1
    broker.run(lambda body: None)
    assert broker.processed == ["m1"]
    assert broker.dead == []
