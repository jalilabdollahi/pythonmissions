# Mission 103 - Incident Queue Order
# Orders open incidents for the on-call board by priority, then name.
def sort_incidents(incidents):
    return sorted(
        incidents,
        key=lambda item: (item["priority"], item["name"].lower()),
        reverse=True,
    )


def top_names(incidents, limit):
    ordered = sort_incidents(incidents)
    return [item["name"] for item in ordered[:limit]]


def count_by_priority(incidents):
    counts = {}
    for item in incidents:
        counts[item["priority"]] = counts.get(item["priority"], 0) + 1
    return counts


if __name__ == "__main__":
    sample = [
        {"name": "checkout-latency", "priority": 3},
        {"name": "auth-errors", "priority": 3},
        {"name": "report-delay", "priority": 1},
    ]
    for entry in sort_incidents(sample):
        print(entry["priority"], entry["name"])
