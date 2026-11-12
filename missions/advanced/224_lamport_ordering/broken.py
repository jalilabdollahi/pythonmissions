# Mission 224 - Audit Log Interleaver
# Lamport clocks for interleaving audit logs from workers without a shared clock.
from collections import namedtuple

Event = namedtuple("Event", ["time", "node", "payload"])


class LamportNode:
    def __init__(self, node_id):
        self.node_id = node_id
        self.time = 0

    def _stamp(self, payload):
        event = Event(self.time, self.node_id, payload)
        self.time += 1
        return event

    def local_event(self, payload):
        return self._stamp(payload)

    def send(self, payload):
        return self._stamp(payload)

    def receive(self, message, payload):
        self.time = message.time
        return self._stamp(payload)


def order_key(event):
    return (event.time, str(event.node))


def total_order(events):
    return sorted(events, key=order_key)


def merge_logs(*logs):
    seen = {}
    for log in logs:
        for event in log:
            seen.setdefault(event.time, event)
    return total_order(seen.values())


def causally_precedes(a, b):
    return a.time < b.time


def render(events):
    lines = []
    for event in total_order(events):
        lines.append(f"[{event.time:04d}] worker-{event.node}: {event.payload}")
    return lines


def by_node(events):
    grouped = {}
    for event in total_order(events):
        grouped.setdefault(event.node, []).append(event)
    return grouped


def window(events, start, end):
    return [e for e in total_order(events) if start <= e.time <= end]


def last_seen(events):
    latest = {}
    for event in events:
        if event.node not in latest or event.time > latest[event.node]:
            latest[event.node] = event.time
    return latest
