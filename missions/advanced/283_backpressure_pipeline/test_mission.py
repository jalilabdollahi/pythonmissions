import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import BoundedBuffer, Pipeline, Stage


def test_reject_policy_never_exceeds_capacity():
    buf = BoundedBuffer(2, "reject")
    results = [buf.offer(i) for i in range(4)]
    assert results == [True, True, False, False]
    assert len(buf) == 2, "capacity is a hard limit"
    assert buf.rejected == 2 and buf.accepted == 2


def test_drop_oldest_evicts_the_front_of_the_queue():
    buf = BoundedBuffer(3, "drop_oldest")
    for i in range(5):
        assert buf.offer(i) is True
    assert list(buf.items) == [2, 3, 4], "the oldest items are the ones shed"


def test_every_eviction_is_counted():
    buf = BoundedBuffer(2, "drop_oldest")
    for i in range(5):
        buf.offer(i)
    assert buf.dropped == 3
    assert buf.rejected == 0
    assert buf.accepted == 5


def test_unknown_policy_is_rejected():
    try:
        BoundedBuffer(1, "block_forever")
    except ValueError:
        return
    raise AssertionError("an unknown policy must raise ValueError")


def test_items_flow_through_all_stages_in_order():
    pipe = Pipeline([
        Stage("parse", lambda x: x + 1, 4),
        Stage("enrich", lambda x: x * 10, 4),
    ])
    for i in range(3):
        assert pipe.push(i)
    assert pipe.drain() == [10, 20, 30]


def test_refused_handoff_keeps_item_upstream():
    pipe = Pipeline([
        Stage("parse", str.upper, 5),
        Stage("publish", lambda x: x, 0, "reject"),  # downstream that accepts nothing
    ])
    pipe.push("a")
    for _ in range(3):
        pipe.step()
    assert list(pipe.stages[0].buffer.items) == ["a"], "a refused item stays queued upstream"
    assert pipe.stages[1].buffer.rejected == 3, "and is retried on every step"
    assert pipe.output == []


def test_stats_report_per_stage_counters():
    pipe = Pipeline([Stage("only", lambda x: x, 1, "reject")])
    pipe.push(1)
    pipe.push(2)
    assert pipe.stats()["only"] == {"queued": 1, "accepted": 1, "rejected": 1, "dropped": 0}
