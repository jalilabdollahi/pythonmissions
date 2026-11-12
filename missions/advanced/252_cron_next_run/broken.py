# Mission 252 - Cron Next Run
# Computes the next fire time for a standard five-field cron expression.
from datetime import datetime, timedelta

FIELDS = [("minute", 0, 59), ("hour", 0, 23), ("day", 1, 31), ("month", 1, 12), ("weekday", 0, 7)]


def _parse_field(text, name, lo, hi):
    values = set()
    for part in text.split(","):
        step = 1
        if "/" in part:
            part, step_text = part.split("/", 1)
            step = int(step_text)
            if step < 1:
                raise ValueError(f"{name}: step must be positive")
        if part == "*":
            start, end = lo, hi
        elif "-" in part:
            first, last = part.split("-", 1)
            start, end = int(first), int(last)
        else:
            start = int(part)
            end = hi if step > 1 else start
        if start < lo or end > hi or start > end:
            raise ValueError(f"{name}: {part!r} is outside {lo}-{hi}")
        values.update(range(start, end, step))
    if name == "weekday":
        values = {v % 7 for v in values}
    return values


class CronSpec:
    def __init__(self, expression):
        parts = expression.split()
        if len(parts) != 5:
            raise ValueError("expected five fields: minute hour day month weekday")
        parsed = [_parse_field(p, n, lo, hi) for p, (n, lo, hi) in zip(parts, FIELDS)]
        self.minutes, self.hours, self.days, self.months, self.weekdays = parsed
        self.day_is_star = parts[2].startswith("*")
        self.weekday_is_star = parts[4].startswith("*")

    def day_matches(self, moment):
        cron_weekday = moment.weekday()
        day_ok = moment.day in self.days
        weekday_ok = cron_weekday in self.weekdays
        if self.day_is_star and self.weekday_is_star:
            return True
        if self.day_is_star:
            return weekday_ok
        if self.weekday_is_star:
            return day_ok
        return day_ok and weekday_ok

    def matches(self, moment):
        return (
            moment.minute in self.minutes
            and moment.hour in self.hours
            and moment.month in self.months
            and self.day_matches(moment)
        )


def _first_of_next_month(moment):
    if moment.month == 12:
        return datetime(moment.year + 1, 1, 1)
    return datetime(moment.year, moment.month + 1, 1)


def next_run(spec, after):
    """First matching minute strictly after `after` (seconds are ignored)."""
    candidate = after.replace(second=0, microsecond=0)
    while candidate.year <= after.year + 8:
        if candidate.month not in spec.months:
            candidate = _first_of_next_month(candidate)
        elif not spec.day_matches(candidate):
            candidate = candidate.replace(hour=0, minute=0) + timedelta(days=1)
        elif candidate.hour not in spec.hours:
            candidate = candidate.replace(minute=0) + timedelta(hours=1)
        elif candidate.minute not in spec.minutes:
            candidate += timedelta(minutes=1)
        else:
            return candidate
    raise ValueError("expression never fires")


def upcoming(expression, after, count):
    spec = CronSpec(expression)
    runs = []
    for _ in range(count):
        after = next_run(spec, after)
        runs.append(after)
    return runs
