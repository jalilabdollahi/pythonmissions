# Mission 101 - Multi-Source Log Aggregator
# Fixed solution
import heapq
from datetime import datetime

LOG_FORMAT = "%Y-%m-%dT%H:%M:%S"

def parse_ts(log_line):
    ts_str = log_line.split(" ")[0]
    return datetime.strptime(ts_str, LOG_FORMAT)

def sort_logs(logs):
    return sorted(logs, key=parse_ts)

def aggregate_logs(*log_streams):
    sorted_streams = [sort_logs(s) for s in log_streams]
    return list(heapq.merge(*sorted_streams, key=parse_ts))
