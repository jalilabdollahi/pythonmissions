import pytest, sys
sys.path.insert(0, ".")
from broken import record_latency, get_histogram

def test_buckets_sorted():
    h = get_histogram()
    buckets = h.buckets
    assert buckets == sorted(buckets)

def test_records_in_seconds():
    record_latency(500)  # 500ms = 0.5s
    h = get_histogram()
    last_obs = h.observations[-1]
    assert last_obs == pytest.approx(0.5)
