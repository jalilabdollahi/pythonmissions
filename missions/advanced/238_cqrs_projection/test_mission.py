import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import DeployBoard


def ev(stream, version, kind, release=None):
    return {"stream": stream, "version": version, "type": kind, "release": release}


def test_in_order_events_build_the_row():
    board = DeployBoard()
    assert board.handle(ev("api", 1, "deploy_started", "v2")) == "applied"
    assert board.handle(ev("api", 2, "deploy_succeeded", "v2")) == "applied"
    assert board.view["api"] == {"status": "healthy", "release": "v2", "failures": 0}


def test_duplicate_event_is_ignored_even_at_the_current_version():
    board = DeployBoard()
    board.handle(ev("api", 1, "deploy_failed"))
    assert board.handle(ev("api", 1, "deploy_failed")) == "duplicate"
    assert board.view["api"]["failures"] == 1, "a redelivered failure must not count twice"
    assert board.duplicates == 1


def test_old_event_is_a_duplicate():
    board = DeployBoard()
    for v, kind in ((1, "deploy_started"), (2, "deploy_failed"), (3, "deploy_started")):
        board.handle(ev("api", v, kind, "v3"))
    assert board.handle(ev("api", 2, "deploy_failed")) == "duplicate"
    assert board.status_of("api") == "deploying"


def test_early_event_is_buffered_until_the_gap_fills():
    board = DeployBoard()
    board.handle(ev("api", 1, "deploy_started", "v2"))
    assert board.handle(ev("api", 3, "deploy_succeeded", "v2")) == "buffered"
    assert board.status_of("api") == "deploying", "v3 must wait for v2"
    assert board.buffered_count() == 1
    assert board.handle(ev("api", 2, "deploy_failed")) == "applied"
    assert board.status_of("api") == "healthy"
    assert board.buffered_count() == 0


def test_a_whole_run_of_buffered_events_is_drained():
    board = DeployBoard()
    board.handle(ev("db", 4, "deploy_succeeded", "v9"))
    board.handle(ev("db", 3, "deploy_started", "v9"))
    board.handle(ev("db", 2, "deploy_failed"))
    assert board.handle(ev("db", 1, "deploy_started", "v8")) == "applied"
    assert board.view["db"]["status"] == "healthy"
    assert board.versions["db"] == 4, "versions 2, 3 and 4 must all drain after version 1"


def test_streams_do_not_share_buffers():
    board = DeployBoard()
    board.handle(ev("api", 3, "deploy_succeeded", "v2"))
    board.handle(ev("web", 3, "deploy_failed"))
    board.handle(ev("api", 1, "deploy_started", "v2"))
    board.handle(ev("api", 2, "deploy_started", "v2"))
    assert board.status_of("api") == "healthy"
    assert board.status_of("web") is None, "web v3 is still waiting for v1 and v2"
    assert board.buffered_count() == 1


def test_rebuild_resets_everything_and_replays():
    board = DeployBoard()
    stream = [
        ev("api", 1, "deploy_started", "v2"),
        ev("api", 2, "deploy_failed"),
        ev("web", 1, "service_retired"),
    ]
    for e in stream:
        board.handle(e)
    board.handle(ev("api", 9, "deploy_succeeded", "zzz"))
    view = board.rebuild(stream)
    assert view["api"] == {"status": "failed", "release": "v2", "failures": 1}
    assert board.failing() == ["api"]
    assert board.summary() == {"failed": 1, "retired": 1}
    assert board.releases() == {"api": "v2"}
    assert board.buffered_count() == 0, "stale buffered events must not survive a rebuild"
