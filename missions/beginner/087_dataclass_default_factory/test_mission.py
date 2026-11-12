import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import Release, release_train


def test_new_release_starts_empty():
    r = Release("1.0.0")
    assert r.services == []
    assert r.notes == []


def test_add_service_returns_release_for_chaining():
    r = Release("1.0.0")
    assert r.add_service("api") is r
    assert r.services == ["api"]


def test_releases_do_not_share_service_lists():
    a = Release("1.0.0")
    b = Release("1.1.0")
    a.add_service("api")
    assert b.services == [], "each instance needs its own list: use default_factory"


def test_releases_do_not_share_note_lists():
    a = Release("1.0.0")
    b = Release("1.1.0")
    a.add_note("rollback plan")
    assert b.notes == []


def test_explicit_lists_are_kept():
    r = Release("2.0.0", services=["db"], notes=["x"])
    assert r.services == ["db"] and r.notes == ["x"]


def test_summary_text():
    r = Release("1.2.0").add_service("api").add_service("web").add_note("hotfix")
    assert r.summary() == "1.2.0: api, web (1 notes)"
    assert Release("0.1").summary() == "0.1: none (0 notes)"


def test_release_train_builds_independent_releases():
    train = release_train(["1", "2"])
    train[0].add_service("x")
    assert train[1].services == []
