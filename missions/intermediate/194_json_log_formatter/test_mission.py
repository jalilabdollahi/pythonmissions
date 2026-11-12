import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import broken


import datetime
import io
import json


def emit(name, fn):
    stream = io.StringIO()
    logger = broken.make_logger("json-" + name, stream)
    fn(logger)
    lines = stream.getvalue().splitlines()
    return [json.loads(line) for line in lines], stream.getvalue()


def test_each_record_is_one_json_line_with_core_fields():
    events, raw = emit("core", lambda lg: lg.warning("disk almost full"))
    assert len(raw.splitlines()) == 1
    e = events[0]
    assert e["level"] == "WARNING" and e["logger"] == "json-core" and e["message"] == "disk almost full"
    assert isinstance(e["ts"], float)


def test_percent_arguments_are_applied_to_the_message():
    events, _ = emit("args", lambda lg: lg.info("user %s logged in from %s", "ana", "10.0.0.5"))
    assert events[0]["message"] == "user ana logged in from 10.0.0.5", "use record.getMessage()"


def test_extra_fields_become_top_level_keys():
    events, _ = emit("extra", lambda lg: lg.info("order created", extra={"order_id": 77, "region": "eu"}))
    assert events[0]["order_id"] == 77
    assert events[0]["region"] == "eu"


def test_standard_attributes_do_not_leak_into_output():
    events, _ = emit("std", lambda lg: lg.info("x"))
    assert set(events[0]) == {"level", "logger", "message", "ts"}


def test_unserialisable_extra_is_stringified_not_fatal():
    events, _ = emit("dt", lambda lg: lg.info("when", extra={"day": datetime.date(2024, 1, 2)}))
    assert events[0]["day"] == "2024-01-02", "logging must not raise because of a payload value"


def test_exception_traceback_is_included():
    def work(lg):
        try:
            1 / 0
        except ZeroDivisionError:
            lg.exception("calc failed")

    events, raw = emit("exc", work)
    assert len(raw.splitlines()) == 1, "the traceback must be inside the JSON string"
    assert "ZeroDivisionError" in events[0]["exc"] and "Traceback" in events[0]["exc"]


def test_keys_are_sorted():
    _, raw = emit("sort", lambda lg: lg.info("m", extra={"zeta": 1, "alpha": 2}))
    keys = list(json.loads(raw).keys())
    assert keys == sorted(keys)
