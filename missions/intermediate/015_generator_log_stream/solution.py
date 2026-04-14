# Mission 015 - Log Stream Generator
# Fixed solution

def stream_logs(filepath, level_filter=None):
    with open(filepath, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if level_filter and level_filter not in line:
                continue
            yield line

def count_errors(filepath):
    count = 0
    for line in stream_logs(filepath, "ERROR"):
        count += 1
    return count
