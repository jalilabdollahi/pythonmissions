import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import replica_names, promotion_order


def test_three_replicas_are_generated():
    assert replica_names("db", 3) == ["db-1", "db-2", "db-3"]


def test_last_replica_is_included():
    assert replica_names("quarry-db", 5)[-1] == "quarry-db-5", "the Nth replica must exist"


def test_single_replica():
    assert replica_names("cache", 1) == ["cache-1"]


def test_zero_replicas_is_empty():
    assert replica_names("cache", 0) == []


def test_promotion_order_highest_first():
    assert promotion_order("db", 3) == ["db-3", "db-2", "db-1"]
