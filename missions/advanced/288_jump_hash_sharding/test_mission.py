import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import ShardRouter, distribution, jump_hash, moved_keys, plan_resize, route

KEYS = [f"account-{i:04d}" for i in range(2000)]


def reference_jump(key, buckets):
    b, j = -1, 0
    while j < buckets:
        b = j
        key = (key * 2862933555777941757 + 1) % (1 << 64)
        j = int((b + 1) * ((1 << 31) / ((key >> 33) + 1)))
    return b


def test_matches_the_published_algorithm():
    for key in (0, 1, 2, 12345, 2**40 + 7, 2**63 + 99, 2**64 - 1):
        for buckets in (1, 2, 7, 10, 100):
            assert jump_hash(key, buckets) == reference_jump(key, buckets), (key, buckets)


def test_index_is_always_in_range():
    for n in (1, 2, 3, 5, 8):
        for key in range(1, 700):
            assert 0 <= jump_hash(key * 7919, n) < n, f"key {key} with {n} buckets"


def test_zero_buckets_is_an_error():
    try:
        jump_hash(5, 0)
    except ValueError:
        return
    raise AssertionError("routing to zero shards must raise ValueError")


def test_string_keys_spread_evenly():
    counts = distribution(KEYS, ["s0", "s1", "s2", "s3"])
    assert sum(counts.values()) == len(KEYS)
    assert all(400 <= n <= 600 for n in counts.values()), counts


def test_routing_is_stable():
    shards = ["s0", "s1", "s2"]
    assert [route(k, shards) for k in KEYS[:50]] == [route(k, shards) for k in KEYS[:50]]
    assert route("account-0001", ["only"]) == "only"


def test_adding_a_shard_moves_only_keys_onto_the_new_shard():
    old = ["db-3", "db-5", "db-7", "db-9"]
    new = old + ["db-1"]  # sorts before every existing name, but is appended
    moved = moved_keys(KEYS, old, new)
    assert all(route(k, new) == "db-1" for k in moved), "keys may only move to the new shard"
    assert 0.1 < len(moved) / len(KEYS) < 0.3, "about 1/5 of keys should move"


def test_plan_resize_reports_targets():
    plan = plan_resize(KEYS, ["a", "b"], ["a", "b", "c"])
    assert list(plan["targets"]) == ["c"]
    assert plan["moved"] == plan["targets"]["c"]
    assert 0.25 < plan["fraction"] < 0.42


def test_router_appends_shards_and_rejects_duplicates():
    router = ShardRouter(["a", "b"])
    plan = router.add_shard("c", KEYS)
    assert router.shards == ("a", "b", "c")
    assert plan["targets"].keys() == {"c"}
    assert router.route(KEYS[0]) in {"a", "b", "c"}
    try:
        router.add_shard("a")
    except ValueError:
        return
    raise AssertionError("adding an existing shard must raise ValueError")
