# Mission 204 - Disk Alert Levels
# Map disk usage percentages to alert levels with a bisect-based scale.
import bisect


def build_scale(cutoffs):
    pairs = list(cutoffs.items())
    bounds = [bound for _, bound in pairs]
    labels = ["ok"] + [level for level, _ in pairs]
    return bounds, labels


def classify(scale, pct):
    if pct < 0:
        raise ValueError(f"invalid usage: {pct}")
    bounds, labels = scale
    return labels[bisect.bisect_left(bounds, pct)]


def classify_all(scale, volumes):
    return {name: classify(scale, pct) for name, pct in volumes.items()}


def describe(scale):
    bounds, labels = scale
    return [f"{level} >= {bound}%" for level, bound in zip(labels[1:], bounds)]


def escalations(scale, before, after):
    worse = []
    _, labels = scale
    for name, pct in sorted(after.items()):
        old = classify(scale, before.get(name, 0))
        new = classify(scale, pct)
        if labels.index(new) > labels.index(old):
            worse.append((name, old, new))
    return worse


def worst_level(scale, volumes):
    _, labels = scale
    levels = classify_all(scale, volumes).values()
    return max(levels, key=labels.index)


if __name__ == "__main__":
    scale = build_scale({"warn": 70, "critical": 85, "page": 95})
    print(classify_all(scale, {"/var": 72, "/data": 97}))
