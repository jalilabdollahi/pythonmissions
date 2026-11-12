import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import LogTail, attach_to_ticket


def test_buffer_never_exceeds_capacity():
    buf = LogTail(3)
    for i in range(10):
        buf.add(f"line {i}")
    assert len(buf) == 3, "a ring buffer drops the oldest line when full"


def test_keeps_the_newest_lines_in_order():
    buf = LogTail(3)
    for i in range(10):
        buf.add(f"line {i}")
    assert buf.tail(3) == ["line 7", "line 8", "line 9"]


def test_tail_returns_only_the_last_n():
    buf = LogTail(5)
    for word in ["a", "b", "c", "d"]:
        buf.add(word)
    assert buf.tail(2) == ["c", "d"]
    assert buf.tail(10) == ["a", "b", "c", "d"]


def test_tail_zero_is_empty_not_everything():
    buf = LogTail(5)
    buf.add("x")
    assert buf.tail(0) == []


def test_chunk_with_trailing_newline_has_no_blank_line():
    buf = LogTail(10)
    buf.add_chunk("boot\nready\n")
    assert buf.tail(10) == ["boot", "ready"]


def test_add_strips_newline():
    buf = LogTail(2)
    buf.add("hello\n")
    assert buf.ticket_text() == "hello"


def test_ticket_contains_header_and_latest_lines():
    buf = LogTail(3)
    buf.add_chunk("boot\nready\nserving\ncrash\n")
    text = attach_to_ticket(buf, "worker-7 died", n=2)
    assert text == "worker-7 died\n--- last 2 lines ---\nserving\ncrash"


def test_last_and_clear():
    buf = LogTail(2)
    assert buf.last() is None
    buf.add("a")
    buf.add("b")
    assert buf.last() == "b"
    buf.clear()
    assert len(buf) == 0


def test_capacity_must_be_positive():
    with pytest.raises(ValueError):
        LogTail(0)
