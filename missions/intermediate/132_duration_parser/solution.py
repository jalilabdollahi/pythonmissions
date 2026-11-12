# Mission 132 - Human Duration Parser (solution)
# Convert strings like "1h30m15s" into seconds and back.
import re

UNITS = {"w": 604800, "d": 86400, "h": 3600, "m": 60, "s": 1}
TOKEN_RE = re.compile(r"(\d+)([wdhms])")
FULL_RE = re.compile(r"(?:\d+[wdhms])+")


def parse_duration(text):
    text = text.strip()
    if text.isdigit():
        return int(text)
    if not FULL_RE.fullmatch(text):
        raise ValueError(f"invalid duration: {text!r}")
    total = 0
    for number, unit in TOKEN_RE.findall(text):
        total += int(number) * UNITS[unit]
    if total == 0 and not text.startswith("0"):
        raise ValueError(f"invalid duration: {text!r}")
    return total


def format_duration(seconds):
    if seconds == 0:
        return "0s"
    parts = []
    for unit in ("w", "d", "h", "m", "s"):
        count, seconds = divmod(seconds, UNITS[unit])
        if count:
            parts.append(f"{count}{unit}")
    return "".join(parts)
