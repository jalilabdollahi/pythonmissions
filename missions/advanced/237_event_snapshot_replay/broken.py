# Mission 237 - Seat Pool Rehydration
# Rebuild a licence seat pool from a snapshot plus the events recorded after it.


def empty_pool():
    return {"seats": 0, "assigned": set()}


def apply_event(state, event):
    kind = event["type"]
    data = event["data"]
    if kind == "seats_added":
        state["seats"] += data["count"]
    elif kind == "seat_assigned":
        state["assigned"].add(data["user"])
    elif kind == "seat_revoked":
        state["assigned"].discard(data["user"])
    else:
        raise ValueError(f"unknown event type {kind!r}")
    return state


def take_snapshot(state, version):
    return {
        "version": version,
        "state": {"seats": state["seats"], "assigned": state["assigned"]},
    }


def rehydrate(snapshot, events):
    if snapshot is None:
        version = 0
        state = empty_pool()
    else:
        version = snapshot["version"]
        state = {
            "seats": snapshot["state"]["seats"],
            "assigned": set(snapshot["state"]["assigned"]),
        }
    newer = [e for e in events if e["version"] >= version]
    for event in newer:
        apply_event(state, event)
        version = event["version"]
    return state, version


def free_seats(state):
    return state["seats"] - len(state["assigned"])


def should_snapshot(version, last_snapshot_version, every=100):
    return version - last_snapshot_version >= every


class PoolStore:
    def __init__(self):
        self.events = []
        self.snapshot = None

    def append(self, kind, **data):
        version = len(self.events) + 1
        self.events.append({"version": version, "type": kind, "data": data})
        return version

    def load(self):
        return rehydrate(self.snapshot, self.events)

    def checkpoint(self):
        state, version = self.load()
        self.snapshot = take_snapshot(state, version)
        return version
