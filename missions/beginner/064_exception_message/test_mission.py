import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import broken


def test_valid_port_has_empty_reason():
    assert broken.check_port("443") == (True, "")


def test_out_of_range_reason_comes_from_the_exception():
    ok, reason = broken.check_port("70000")
    assert ok is False
    assert reason == "port 70000 is out of range", "use str(error) to read the message"


def test_non_numeric_reason_mentions_the_text():
    ok, reason = broken.check_port("abc")
    assert ok is False
    assert "abc" in reason


def test_failure_report_lists_only_bad_values():
    report = broken.failure_report(["80", "0", "22"])
    assert report == ["0: port 0 is out of range"]


def test_all_ok():
    assert broken.all_ok(["1", "65535"]) is True
    assert broken.all_ok(["1", "65536"]) is False
