import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import by_node, window, Event, LamportNode, causally_precedes, last_seen, merge_logs, render, total_order


def test_first_event_gets_time_one():
    node = LamportNode(1)
    assert node.local_event("boot").time == 1
    assert node.local_event("ready").time == 2


def test_receive_is_strictly_after_the_message():
    sender = LamportNode(9)
    receiver = LamportNode(1)
    for i in range(5):
        sender.local_event(f"warmup-{i}")
    msg = sender.send("payment captured")
    reply = receiver.receive(msg, "refund issued")
    assert reply.time == msg.time + 1, "receive must jump to max(local, remote) + 1"
    assert causally_precedes(msg, reply)
    assert total_order([reply, msg]) == [msg, reply], "cause must sort before effect"


def test_receiver_with_larger_clock_keeps_counting_forward():
    receiver = LamportNode(3)
    for i in range(10):
        receiver.local_event(f"e{i}")
    msg = Event(2, 7, "old news")
    assert receiver.receive(msg, "ack").time == 11


def test_ties_break_by_numeric_node_id():
    a = Event(5, 2, "from-2")
    b = Event(5, 10, "from-10")
    assert total_order([b, a]) == [a, b], "node 2 < node 10 numerically, not as strings"


def test_order_is_identical_regardless_of_log_arrival_order():
    log_x = [Event(1, 1, "a"), Event(2, 1, "b")]
    log_y = [Event(1, 2, "c"), Event(2, 2, "d")]
    assert merge_logs(log_x, log_y) == merge_logs(log_y, log_x)
    assert [e.payload for e in merge_logs(log_x, log_y)] == ["a", "c", "b", "d"]


def test_merge_keeps_simultaneous_events_from_different_nodes():
    one = [Event(4, 1, "x")]
    two = [Event(4, 2, "y")]
    merged = merge_logs(one, two)
    assert len(merged) == 2, "same timestamp but different node is a different event"


def test_merge_removes_true_duplicates():
    e = Event(3, 5, "dup")
    assert merge_logs([e], [e], [Event(3, 5, "dup")]) == [e]


def test_window_and_by_node():
    events = [Event(t, t % 2, f"e{t}") for t in range(1, 7)]
    assert [e.time for e in window(events, 2, 4)] == [2, 3, 4]
    assert [e.time for e in by_node(events)[1]] == [1, 3, 5]


def test_render_and_last_seen():
    events = [Event(2, 1, "b"), Event(1, 2, "a")]
    assert render(events) == ["[0001] worker-2: a", "[0002] worker-1: b"]
    assert last_seen(events + [Event(7, 1, "z")]) == {1: 7, 2: 1}
