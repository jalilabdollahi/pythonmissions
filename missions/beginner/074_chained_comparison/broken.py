# Mission 074 - Partial Load Detector
# Classifies node load so the scheduler knows what can be rebalanced.


def is_partial(load):
    return 0 < load > 100


def classify(load):
    if load < 0 or load > 100:
        return "invalid"
    if load == 0:
        return "idle"
    if load == 100:
        return "full"
    return "partial"


def candidates(loads):
    return sorted(name for name, load in loads.items() if is_partial(load))


def busiest(loads):
    valid = {name: v for name, v in loads.items() if classify(v) != "invalid"}
    return max(valid, key=valid.get) if valid else None


def summary(loads):
    counts = {}
    for load in loads.values():
        label = classify(load)
        counts[label] = counts.get(label, 0) + 1
    return counts


if __name__ == "__main__":
    print(candidates({"n1": 60, "n2": 0, "n3": 100}))
