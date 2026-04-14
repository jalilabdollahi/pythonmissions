# Mission 118 - Log Parser State Machine
# Fixed solution

def parse_multiline_logs(text):
    entries = []
    current = None

    for line in text.splitlines():
        if not line:
            continue
        is_continuation = line[0].isspace()
        if is_continuation:
            if current is not None:
                current["trace"].append(line.strip())
        else:
            if current is not None:
                entries.append(current)
            current = {"message": line, "trace": []}

    if current is not None:
        entries.append(current)
    return entries
