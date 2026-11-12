import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import ORSet, merge_all, snapshot, sync


def test_add_and_contains():
    s = ORSet("a")
    s.add("db-1")
    assert s.contains("db-1") and not s.contains("db-2")
    assert s.elements() == ["db-1"]


def test_every_add_gets_a_unique_tag():
    s = ORSet("a")
    assert s.add("db-1") != s.add("db-1")


def test_readd_after_remove_is_visible_again():
    s = ORSet("a")
    s.add("db-1")
    s.remove("db-1")
    assert not s.contains("db-1")
    s.add("db-1")
    assert s.contains("db-1"), "the new add has a fresh tag the tombstone never covered"


def test_remove_covers_all_observed_tags():
    s = ORSet("a")
    s.add("db-1")
    s.add("db-1")
    s.add("db-1")
    assert s.remove("db-1")
    assert not s.contains("db-1"), "every add we have seen must be removed"


def test_removing_unknown_element_is_a_noop():
    s = ORSet("a")
    assert s.remove("ghost") is False
    assert s.state_size() == 0


def test_removals_propagate_through_merge():
    a, b = ORSet("a"), ORSet("b")
    a.add("db-1")
    b.merge(a)
    a.remove("db-1")
    b.merge(a)
    assert not b.contains("db-1"), "tombstones must be merged along with adds"


def test_concurrent_add_beats_remove():
    a, b = ORSet("a"), ORSet("b")
    a.add("db-1")
    b.merge(a)
    a.remove("db-1")
    b.add("db-1")
    sync(a, b)
    assert a.elements() == b.elements() == ["db-1"], "add-wins: b never saw a's remove"


def test_merge_unions_tags_instead_of_replacing_them():
    a, b = ORSet("a"), ORSet("b")
    a.add("x")
    b.add("x")
    a.merge(b)
    b.remove("x")
    a.merge(b)
    assert a.contains("x"), "a's own tag was never observed by b, so it survives b's remove"


def test_compact_drops_dead_tags():
    a = ORSet("a")
    a.add("x")
    a.add("y")
    a.remove("x")
    a.compact()
    assert a.elements() == ["y"]
    assert a.state_size() == 1

def test_merge_all_and_snapshot():
    a, b = ORSet("a"), ORSet("b")
    a.add("x")
    b.add("y")
    b.add("z")
    b.remove("z")
    m = merge_all("m", a, b)
    assert m.elements() == ["x", "y"]
    assert snapshot(m) == {"replica": "m", "elements": ["x", "y"], "tags": 4}
