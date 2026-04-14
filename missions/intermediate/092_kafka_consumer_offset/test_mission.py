import pytest, sys
sys.path.insert(0, ".")
from broken import OffsetTracker

def test_process_commits_after():
    tracker = OffsetTracker()
    processed = []
    def handler(msg): processed.append(msg)
    tracker.process_message("p0", 5, handler, "hello")
    assert tracker.get_committed("p0") == 5
    assert "hello" in processed

def test_lag():
    tracker = OffsetTracker()
    tracker._pending["p0"] = 10
    tracker._committed["p0"] = 7
    assert tracker.lag("p0") == 3
