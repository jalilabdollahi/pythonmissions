# Mission 118 - Log Parser State Machine
# Fix the 2 bugs in this script.

def parse_multiline_logs(text):
    """Parse logs where stack traces are indented continuation lines."""
    entries = []
    current = None

    for line in text.splitlines():
        if not line:
            continue
        is_continuation = line[0].isspace()  # indented = continuation
        if is_continuation:
            if current is not None:
                current["trace"].append(line.strip())
            # BUG 1: if current is None and we get a continuation, skip
        else:
            if current is not None:
                entries.append(current)
            # BUG 2: new top-level line should create a new entry
            entries.append({"message": line, "trace": []})  # wrong: should set current, not append yet

    if current is not None:
        entries.append(current)
    return entries
