import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import BloomFilter, optimal_bits, optimal_hashes, capacity_report, screen


def test_sizing_matches_textbook_values():
    assert optimal_bits(1000, 0.01) == 9586
    assert optimal_hashes(9586, 1000) == 7, "k = (m/n) ln 2 = 6.64 rounds to 7"
    assert optimal_bits(100, 0.5) == 145
    assert optimal_hashes(145, 100) == 1


def test_invalid_parameters_are_rejected():
    for n, p in ((0, 0.1), (10, 0), (10, 1), (10, 1.5)):
        with pytest.raises(ValueError):
            BloomFilter(n, p)


def test_no_false_negatives():
    bloom = BloomFilter(500, 0.01)
    ids = [f"scan-{i:06d}" for i in range(500)]
    for scan_id in ids:
        bloom.add(scan_id)
    missing = [i for i in ids if not bloom.contains(i)]
    assert missing == [], "an inserted item must always be reported present"


def test_empty_filter_contains_nothing():
    bloom = BloomFilter(100, 0.01)
    assert not any(bloom.contains(f"x{i}") for i in range(200)), "all bits are zero: need ALL of them set"


def test_false_positive_rate_stays_near_target():
    bloom = BloomFilter(1000, 0.01)
    for i in range(1000):
        bloom.add(f"scan-{i:06d}")
    probes = 5000
    fp = sum(bloom.contains(f"other-{i:06d}") for i in range(probes))
    assert fp / probes < 0.02, f"measured fp rate {fp / probes:.3f} is far above the 1% target"


def test_probe_positions_are_spread_not_consecutive():
    bloom = BloomFilter(1000, 0.01)
    positions = bloom._positions("scan-000001")
    steps = {(b - a) % bloom.m for a, b in zip(positions, positions[1:])}
    assert steps != {1}, "probes must step by a hash-derived stride, not by 1"


def test_union_contains_items_of_both_filters():
    a, b = BloomFilter(100, 0.01), BloomFilter(100, 0.01)
    a.add("alpha")
    b.add("beta")
    both = a.union(b)
    assert both.contains("alpha") and both.contains("beta")
    with pytest.raises(ValueError):
        a.union(BloomFilter(200, 0.01))


def test_estimated_rate_and_screening():
    bloom = BloomFilter(1000, 0.01)
    for i in range(1000):
        bloom.add(f"scan-{i:06d}")
    assert 0.005 < bloom.estimated_fp_rate() < 0.02
    assert 0.3 < bloom.fill_ratio() < 0.7
    assert capacity_report(bloom) == {"bits": 9586, "hashes": 7, "bytes": 1199, "load": 1.0}
    maybe, new = screen(bloom, ["scan-000010", "never-seen-before-1"])
    assert maybe == ["scan-000010"] and new == ["never-seen-before-1"]
