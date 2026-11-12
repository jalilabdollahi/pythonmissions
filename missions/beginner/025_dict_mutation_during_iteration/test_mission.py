import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import purge_expired, active_tokens


def make_store():
    return {"tok-a": 100, "tok-b": 500, "tok-c": 90, "tok-d": 200}


def test_expired_tokens_are_removed_in_place():
    store = make_store()
    purge_expired(store, 200)
    assert sorted(store) == ["tok-b"], "the same dict must lose its expired tokens"


def test_returns_number_removed():
    assert purge_expired(make_store(), 200) == 3


def test_nothing_expired_changes_nothing():
    store = make_store()
    assert purge_expired(store, 50) == 0
    assert len(store) == 4


def test_everything_expired_empties_the_store():
    store = make_store()
    assert purge_expired(store, 10_000) == 4
    assert store == {}


def test_active_tokens_sorted():
    assert active_tokens(make_store(), 150) == ["tok-b", "tok-d"]
