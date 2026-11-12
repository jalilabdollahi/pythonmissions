# Mission 136 - Rack Hostlists
# Expand compact host patterns such as web[01-03].dc1 into hostnames.
import re

GROUP_RE = re.compile(r"^(?P<head>[^\[\]]*)\[(?P<body>[^\[\]]+)\](?P<tail>[^\[\]]*)$")


def split_top_level(spec):
    parts, current, depth = [], "", 0
    for char in spec:
        if char == "[":
            depth += 1
        elif char == "]":
            depth -= 1
            if depth < 0:
                raise ValueError(f"unbalanced brackets: {spec!r}")
        if char == "," and depth == 0:
            parts.append(current)
            current = ""
        else:
            current += char
    if depth != 0:
        raise ValueError(f"unbalanced brackets: {spec!r}")
    parts.append(current)
    return [p.strip() for p in parts if p.strip()]


def expand_items(body):
    numbers = []
    for item in body.split(","):
        if "-" in item:
            low_text, high_text = item.split("-", 1)
            width = 0
            for n in range(int(low_text), int(high_text)):
                numbers.append(f"{n:0{width}d}")
        else:
            numbers.append(item)
    return numbers


def expand_pattern(pattern):
    match = GROUP_RE.match(pattern)
    if match is None:
        if "[" in pattern or "]" in pattern:
            raise ValueError(f"bad pattern: {pattern!r}")
        return [pattern]
    return [match["head"] + n + match["tail"] for n in expand_items(match["body"])]


def expand_hostlist(spec):
    hosts = []
    for pattern in spec.split(","):
        hosts.extend(expand_pattern(pattern.strip()))
    return hosts
