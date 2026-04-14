import pytest, sys
sys.path.insert(0, ".")
from broken import allocate_list, profile_memory

def test_profiler_records_peak():
    allocate_list(10000)
    assert allocate_list.last_peak_kb >= 0

def test_peak_in_kb_not_bytes():
    allocate_list(1000000)
    # Peak should be in KB — if it were bytes it would be > 1,000,000
    # For 1M integers, peak should be a few MB at most (few thousand KB)
    assert allocate_list.last_peak_kb < 100_000  # not in bytes

def test_function_still_works():
    result = allocate_list(5)
    assert result == [0, 1, 4, 9, 16]
