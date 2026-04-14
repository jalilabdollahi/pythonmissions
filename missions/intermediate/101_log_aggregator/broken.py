# Mission 101 - Multi-Source Log Aggregator
# Fix the 2 bugs in this script.
import heapq
from datetime import datetime

LOG_FORMAT = "%Y-%m-%dT%H:%M:%S"

def parse_ts(log_line):
    ts_str = log_line.split(" ")[0]
    return datetime.strptime(ts_str, LOG_FORMAT)

def sort_logs(logs):
    return sorted(logs, key=lambda l: l)  # BUG 1: should sort by parse_ts(l)

def aggregate_logs(*log_streams):
    """Merge multiple sorted log streams into one sorted stream."""
    sorted_streams = [sort_logs(s) for s in log_streams]
    return list(heapq.merge(*sorted_streams))  # BUG 2: heapq.merge compares strings lexicographically — need key
