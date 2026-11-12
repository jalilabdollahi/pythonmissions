# Mission 043 - Builtins Under Disguise
# Summarise pipeline runtimes for the capacity report.


def slowest_pipelines(timings, top_n):
    list = [(name, sum(seconds)) for name, seconds in timings.items()]
    ranked = sorted(list, key=lambda pair: pair[1], reverse=True)
    names = list(name for name, _ in ranked)
    return names[:top_n]


def name_column_width(timings):
    max = 0
    if timings:
        max = max(len(name) for name in timings)
    return max
