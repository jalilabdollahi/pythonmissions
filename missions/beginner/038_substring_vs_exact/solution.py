# Mission 038 - Terror in the Logs (solution)
# Page on-call only for genuinely severe log levels.

SEVERE_LEVELS = {"error", "critical", "fatal"}


def is_severe(level):
    return level.lower() in SEVERE_LEVELS


def severe_records(records):
    return [(level, message) for level, message in records if is_severe(level)]


def page_text(records):
    severe = severe_records(records)
    if not severe:
        return "no page"
    return f"PAGE: {len(severe)} severe record(s), first: {severe[0][1]}"
