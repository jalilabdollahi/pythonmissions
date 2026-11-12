import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import Membership


class Clock:
    def __init__(self):
        self.now = 100.0

    def __call__(self):
        return self.now


def make(me="w1", timeout=5.0):
    clock = Clock()
    return Membership(me, clock, timeout), clock


def test_new_members_are_learned():
    m, _ = make()
    assert m.merge({"w2": ("alive", 0), "w3": ("alive", 2)}) == ["w2", "w3"]
    assert m.alive_members() == ["w1", "w2", "w3"]


def test_stale_incarnation_is_ignored():
    m, _ = make()
    m.merge({"w2": ("alive", 3)})
    assert m.merge({"w2": ("dead", 1)}) == []
    assert m.snapshot()["w2"] == ("alive", 3), "old rumours must not override newer facts"


def test_higher_incarnation_beats_more_severe_status():
    m, _ = make()
    m.merge({"w2": ("dead", 1)})
    m.merge({"w2": ("alive", 2)})
    assert m.snapshot()["w2"] == ("alive", 2), "a rejoin with a higher incarnation wins"


def test_equal_incarnation_uses_severity_and_dead_is_final():
    m, _ = make()
    m.merge({"w2": ("alive", 1)})
    m.merge({"w2": ("suspect", 1)})
    assert m.snapshot()["w2"] == ("suspect", 1)
    m.merge({"w2": ("dead", 1)})
    assert m.snapshot()["w2"] == ("dead", 1)
    m.merge({"w2": ("suspect", 1)})
    m.merge({"w2": ("alive", 1)})
    assert m.snapshot()["w2"] == ("dead", 1), "dead must not be downgraded at the same incarnation"


def test_refutation_outranks_the_accusation():
    m, _ = make("w1")
    m.merge({"w1": ("suspect", 4)})
    assert m.snapshot()["w1"] == ("alive", 5), "must exceed the accuser's incarnation"
    assert m.merge({"w1": ("suspect", 4)}) == [], "the same rumour is now stale"


def test_suspect_expires_exactly_at_timeout():
    m, clock = make(timeout=5.0)
    m.merge({"w2": ("alive", 0)})
    assert m.suspect("w2")
    clock.now += 4.9
    assert m.expire_suspects() == []
    clock.now += 0.1
    assert m.expire_suspects() == ["w2"], "elapsed == timeout counts as expired"
    assert m.snapshot()["w2"] == ("dead", 0)


def test_summary_and_quorum():
    m, _ = make()
    m.merge({"w2": ("alive", 0), "w3": ("dead", 0), "w4": ("suspect", 0)})
    assert m.summary() == {"alive": 2, "suspect": 1, "dead": 1}
    assert not m.quorum_alive(), "2 of 4 is not a majority"


def test_suspect_is_only_raised_for_alive_members():
    m, _ = make()
    assert not m.suspect("nobody")
    m.merge({"w2": ("dead", 0)})
    assert not m.suspect("w2")
