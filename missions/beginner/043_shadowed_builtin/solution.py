# Mission 043 - Builtins Under Disguise (solution)
# Summarise pipeline runtimes for the capacity report.


def slowest_pipelines(timings, top_n):
    totals = [(name, sum(seconds)) for name, seconds in timings.items()]
    ranked = sorted(totals, key=lambda pair: pair[1], reverse=True)
    names = list(name for name, _ in ranked)
    return names[:top_n]


def name_column_width(timings):
    widest = 0
    if timings:
        widest = max(len(name) for name in timings)
    return widest
