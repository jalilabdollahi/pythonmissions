# Mission 143 - StatsD Intake (solution)
# Parse StatsD datagrams and aggregate them into counters, gauges and timers.

TYPES = {"c": "counter", "g": "gauge", "ms": "timer"}


def parse_statsd(line):
    try:
        name, rest = line.strip().split(":", 1)
        fields = rest.split("|")
        raw, kind = fields[0], fields[1]
    except (ValueError, IndexError):
        raise ValueError(f"malformed statsd line: {line!r}")
    if kind not in TYPES or not name:
        raise ValueError(f"unsupported statsd line: {line!r}")
    rate = 1.0
    for extra in fields[2:]:
        if extra.startswith("@"):
            rate = float(extra[1:])
    try:
        value = float(raw)
    except ValueError:
        raise ValueError(f"bad value in {line!r}")
    delta = kind == "g" and raw[0] in "+-"
    if kind == "c":
        value = value / rate
    return {"name": name, "type": kind, "value": value, "delta": delta}


def aggregate(lines):
    result = {"counters": {}, "gauges": {}, "timers": {}}
    for line in lines:
        item = parse_statsd(line)
        name, value = item["name"], item["value"]
        if item["type"] == "c":
            result["counters"][name] = result["counters"].get(name, 0) + value
        elif item["type"] == "g":
            if item["delta"]:
                result["gauges"][name] = result["gauges"].get(name, 0) + value
            else:
                result["gauges"][name] = value
        else:
            result["timers"].setdefault(name, []).append(value)
    return result
