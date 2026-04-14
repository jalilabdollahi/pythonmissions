# Mission 015 - Log Stream Generator
# Fix the 2 bugs in this script.

def stream_logs(filepath, level_filter=None):
    with open(filepath, "rb") as f:  # BUG 1: should be "r" not "rb"
        for line in f:
            line = line.strip()
            if not line:
                continue
            if level_filter and level_filter not in line:
                continue
            return line  # BUG 2: should be yield, not return

def count_errors(filepath):
    count = 0
    for line in stream_logs(filepath, "ERROR"):
        count += 1
    return count
