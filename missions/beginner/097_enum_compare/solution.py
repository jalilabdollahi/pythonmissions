# Mission 097 - Alert Levels as Enum (solution)
# Severity handling for the paging service.
from enum import Enum


class Level(Enum):
    DEBUG = "debug"
    WARN = "warn"
    ERROR = "error"


ORDER = [Level.DEBUG, Level.WARN, Level.ERROR]


def parse_level(text):
    return Level(text.strip().lower())


def should_page(raw_level):
    return parse_level(raw_level) == Level.ERROR


def to_wire(level):
    return level.value


def most_severe(raw_levels):
    if not raw_levels:
        return None
    levels = [parse_level(r) for r in raw_levels]
    return max(levels, key=ORDER.index)


if __name__ == "__main__":
    print(should_page("error"), to_wire(Level.WARN), most_severe(["debug", "warn"]))
