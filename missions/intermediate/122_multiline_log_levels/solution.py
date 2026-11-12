# Mission 122 - Stack Trace Census (solution)
# Count log entries per level while ignoring stack-trace continuation lines.
import re

LEVELS = ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")
ALIASES = {"WARN": "WARNING", "FATAL": "CRITICAL"}

ENTRY_RE = re.compile(
    r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3} (?P<level>[A-Z]+) "
)
WORD_RE = re.compile(r"\b(DEBUG|INFO|WARN|WARNING|ERROR|FATAL|CRITICAL)\b")


def detect_level(line):
    match = ENTRY_RE.match(line)
    if match is None:
        return None
    level = match.group(1) if match.re is WORD_RE else match.group("level")
    return ALIASES.get(level, level)


def count_levels(lines):
    counts = dict.fromkeys(LEVELS, 0)
    for line in lines:
        level = detect_level(line)
        if level in counts:
            counts[level] += 1
    return counts


def continuation_lines(lines):
    """Lines that belong to the previous entry rather than starting a new one."""
    return [line for line in lines if ENTRY_RE.match(line) is None and line.strip()]
