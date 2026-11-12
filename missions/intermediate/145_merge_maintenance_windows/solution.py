# Mission 145 - Window Consolidator (solution)
# Merge overlapping or touching maintenance windows into one calendar.
from datetime import datetime

FMT = "%Y-%m-%d %H:%M"


def parse_window(entry):
    start = datetime.strptime(entry["start"], FMT)
    end = datetime.strptime(entry["end"], FMT)
    if end <= start:
        raise ValueError(f"window must end after it starts: {entry}")
    return start, end, entry["team"]


def merge_windows(windows):
    parsed = [parse_window(w) for w in windows]
    parsed.sort(key=lambda item: item[0])
    merged = []
    for start, end, team in parsed:
        if merged and start <= merged[-1]["end"]:
            current = merged[-1]
            current["end"] = max(current["end"], end)
            current["teams"].add(team)
        else:
            merged.append({"start": start, "end": end, "teams": {team}})
    return [
        {
            "start": m["start"].strftime(FMT),
            "end": m["end"].strftime(FMT),
            "teams": sorted(m["teams"]),
        }
        for m in merged
    ]


def in_window(merged, when):
    for window in merged:
        start = datetime.strptime(window["start"], FMT)
        end = datetime.strptime(window["end"], FMT)
        if start <= when < end:
            return True
    return False
