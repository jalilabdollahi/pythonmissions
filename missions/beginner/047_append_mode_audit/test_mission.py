import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import history, record_action


def test_first_entry_is_recorded(tmp_path):
    log = tmp_path / "audit.log"
    record_action(log, "ana", "restart")
    assert history(log) == ["ana restart"]


def test_history_is_kept_when_logging_again(tmp_path):
    log = tmp_path / "audit.log"
    record_action(log, "ana", "restart")
    record_action(log, "raj", "pause")
    assert history(log) == ["ana restart", "raj pause"], "earlier entries must survive new writes"


def test_each_entry_ends_with_newline(tmp_path):
    log = tmp_path / "audit.log"
    record_action(log, "ana", "restart")
    record_action(log, "raj", "pause")
    assert log.read_text(encoding="utf-8") == "ana restart\nraj pause\n"


def test_existing_file_is_extended(tmp_path):
    log = tmp_path / "audit.log"
    log.write_text("old entry\n", encoding="utf-8")
    record_action(log, "mei", "resume")
    assert history(log) == ["old entry", "mei resume"]


def test_history_of_missing_file_is_empty(tmp_path):
    assert history(tmp_path / "nope.log") == []
