import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import IdempotentConsumer, outbox_stats, count_orders, create_order, open_db, pending, relay_once


class Broker:
    def __init__(self, fail_ids=()):
        self.fail_ids = set(fail_ids)
        self.received = []

    def __call__(self, event):
        if event["event_id"] in self.fail_ids:
            raise ConnectionError("broker unavailable")
        self.received.append(event["event_id"])


def test_order_and_event_are_written_together():
    conn = open_db()
    create_order(conn, "o-1", 1999)
    assert count_orders(conn) == 1 and pending(conn) == [1]


def test_failure_after_order_insert_leaves_neither_row():
    conn = open_db()
    with pytest.raises(TypeError):
        create_order(conn, "o-1", 500, metadata={"bad": object()})
    assert count_orders(conn) == 0, "order and outbox row must commit atomically"
    assert pending(conn) == []


def test_relay_publishes_in_order_and_marks_published():
    conn = open_db()
    for i in range(3):
        create_order(conn, f"o-{i}", 100 + i)
    broker = Broker()
    assert relay_once(conn, broker) == 3
    assert broker.received == [1, 2, 3] and pending(conn) == []
    assert relay_once(conn, broker) == 0
    assert outbox_stats(conn) == {"total": 3, "published": 3, "lag": 0}


def test_failed_publish_stays_pending_for_retry():
    conn = open_db()
    create_order(conn, "o-1", 100)
    broker = Broker(fail_ids={1})
    assert relay_once(conn, broker) == 0
    assert pending(conn) == [1], "an unconfirmed event must not be marked published"
    broker.fail_ids.clear()
    assert relay_once(conn, broker) == 1 and broker.received == [1]


def test_relay_stops_at_first_failure_to_keep_order():
    conn = open_db()
    for i in range(4):
        create_order(conn, f"o-{i}", 100)
    broker = Broker(fail_ids={2})
    assert relay_once(conn, broker) == 1
    assert broker.received == [1], "event 3 and 4 must not overtake the failed event 2"
    assert pending(conn) == [2, 3, 4]


def test_relay_respects_batch_size():
    conn = open_db()
    for i in range(5):
        create_order(conn, f"o-{i}", 100)
    broker = Broker()
    assert relay_once(conn, broker, batch_size=2) == 2
    assert pending(conn) == [3, 4, 5]


def test_consumer_ignores_duplicate_deliveries():
    charges = []
    consumer = IdempotentConsumer(lambda e: charges.append(e["event_id"]))
    event = {"event_id": 7, "topic": "order.created", "payload": {}}
    assert consumer.process(event) is True
    assert consumer.process(event) is False
    assert charges == [7], "at-least-once delivery requires an idempotent consumer"


def test_consumer_retries_after_handler_failure():
    attempts = []

    def handler(event):
        attempts.append(event["event_id"])
        if len(attempts) == 1:
            raise RuntimeError("payment API down")

    consumer = IdempotentConsumer(handler)
    event = {"event_id": 9, "topic": "order.created", "payload": {}}
    with pytest.raises(RuntimeError):
        consumer.process(event)
    assert consumer.process(event) is True, "a failed attempt must not count as handled"
    assert attempts == [9, 9]
