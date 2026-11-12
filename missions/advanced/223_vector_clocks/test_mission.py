import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import Replica, dominates, format_clock, compare, merge, receive, resolve_siblings, tick


def test_tick_returns_new_clock_and_leaves_original_alone():
    base = {"eu": 1}
    after = tick(base, "eu")
    assert after == {"eu": 2}
    assert base == {"eu": 1}, "stored versions share dicts; tick must not mutate its input"


def test_merge_is_elementwise_max_over_union():
    assert merge({"eu": 3, "us": 1}, {"us": 2, "ap": 4}) == {"eu": 3, "us": 2, "ap": 4}
    assert merge({}, {"ap": 1}) == {"ap": 1}, "replicas only the second clock knows must survive"


def test_missing_replica_counts_as_zero_when_comparing():
    assert compare({"eu": 1}, {"eu": 1, "us": 1}) == "before"
    assert compare({"eu": 1, "us": 1}, {"eu": 1}) == "after"
    assert compare({"eu": 1, "us": 0}, {"eu": 1}) == "equal"


def test_disjoint_edits_are_concurrent():
    assert compare({"eu": 2}, {"us": 1}) == "concurrent"
    assert compare({"eu": 2, "us": 1}, {"eu": 1, "us": 2}) == "concurrent"


def test_receive_records_a_local_event():
    local = {"eu": 1}
    remote = {"us": 2}
    got = receive(local, remote, "eu")
    assert got == {"eu": 2, "us": 2}
    assert compare(remote, got) == "before", "the receiver's state must strictly dominate the message"


def test_format_and_dominates():
    assert format_clock({"us": 2, "eu": 1, "ap": 0}) == "{eu:1, us:2}"
    assert dominates({"eu": 2}, {"eu": 1}) and not dominates({"eu": 1}, {"eu": 1})


def test_resolve_siblings_drops_dominated_and_duplicate_versions():
    v1 = {"eu": 1}
    v2 = {"eu": 2}
    v3 = {"us": 1}
    v3_copy = {"us": 1}
    kept = resolve_siblings([v1, v2, v3, v3_copy])
    assert kept == [v2, v3], "v1 is dominated by v2; the two v3 copies are one sibling"


def test_replicas_fast_forward_but_flag_conflicts():
    eu, us = Replica("eu"), Replica("us")
    eu.write("on")
    assert us.sync_from(eu) == "fast-forward" and us.value == "on"
    eu.write("off")
    us.write("canary")
    assert us.sync_from(eu) == "conflict"
    assert us.value == "canary", "a conflict must not overwrite either side"
    assert eu.sync_from(us) == "conflict"
