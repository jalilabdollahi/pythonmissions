import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import logging

from broken import check_disk, check_all


def records(caplog):
    return [(r.levelno, r.getMessage()) for r in caplog.records if r.name == "pinecrest.disk"]


def test_warning_is_emitted_for_85_percent(caplog):
    caplog.set_level(logging.INFO)
    check_disk("web-1", 85)
    assert (logging.WARNING, "web-1 disk at 85%, filling up") in records(caplog), "the logger level must not hide warnings"


def test_ninety_seven_percent_is_logged_as_error(caplog):
    caplog.set_level(logging.INFO)
    check_disk("db-1", 97)
    levels = [lvl for lvl, _ in records(caplog)]
    assert levels == [logging.ERROR], "a nearly-full disk is an ERROR, not a WARNING"


def test_healthy_disk_is_logged_at_info(caplog):
    caplog.set_level(logging.INFO)
    check_disk("web-2", 20)
    assert records(caplog) == [(logging.INFO, "web-2 disk at 20%, healthy")]


def test_return_values_name_the_level():
    assert check_disk("a", 10) == "INFO"
    assert check_disk("a", 80) == "WARNING"
    assert check_disk("a", 95) == "ERROR"


def test_debug_records_are_not_expected(caplog):
    caplog.set_level(logging.DEBUG)
    logging.getLogger("pinecrest.disk").debug("noise")
    assert records(caplog) == []


def test_check_all_returns_flagged_hosts():
    assert check_all({"db-1": 97, "web-1": 85, "web-2": 20}) == ["db-1", "web-1"]
