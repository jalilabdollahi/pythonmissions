# Mission 057 - Webhook Payload Mixup (solution)
# Parses incident events delivered as JSON.
import json


def parse_event(raw):
    event = json.loads(raw)
    if "severity" not in event:
        event["severity"] = "unknown"
    return event


def load_events(path):
    with open(path) as handle:
        return json.load(handle)


def severities(events):
    return sorted({event.get("severity", "unknown") for event in events})


def worst_first(events):
    order = {"critical": 0, "high": 1, "low": 2, "unknown": 3}
    return sorted(events, key=lambda e: order.get(e.get("severity", "unknown"), 3))


if __name__ == "__main__":
    import sys

    for item in worst_first(load_events(sys.argv[1])):
        print(item["id"], item.get("severity"))
