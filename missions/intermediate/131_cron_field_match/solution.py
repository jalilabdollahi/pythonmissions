# Mission 131 - Cron Field Matcher (solution)
# Match values against cron fields: *, lists, ranges, and steps.
from datetime import datetime


def part_matches(part, value, lo, hi):
    step = 1
    if "/" in part:
        part, step_text = part.split("/", 1)
        step = int(step_text)
    if part == "*":
        start, end = lo, hi
    elif "-" in part:
        a, b = part.split("-", 1)
        start, end = int(a), int(b)
    else:
        start = end = int(part)
        if step == 1:
            return value == start
    if not start <= value <= end:
        return False
    return (value - start) % step == 0


def field_matches(field, value, lo, hi):
    for part in field.split(","):
        if part_matches(part, value, lo, hi):
            return True
    return False


def cron_matches(expr, when):
    fields = expr.split()
    if len(fields) != 5:
        raise ValueError("expected 5 cron fields")
    minute, hour, dom, month, dow = fields
    weekday = (when.weekday() + 1) % 7
    return (
        field_matches(minute, when.minute, 0, 59)
        and field_matches(hour, when.hour, 0, 23)
        and field_matches(dom, when.day, 1, 31)
        and field_matches(month, when.month, 1, 12)
        and field_matches(dow, weekday, 0, 6)
    )
