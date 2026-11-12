import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

from broken import (
    InvalidTraceparent,
    child_context,
    continue_or_start,
    format_header,
    is_sampled,
    new_span_id,
    parse,
)

GOOD = "00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01"


class FakeRng:
    def __init__(self, *values):
        self.values = list(values)

    def getrandbits(self, bits):
        return self.values.pop(0)


def test_valid_header_round_trips():
    ctx = parse(GOOD)
    assert ctx.trace_id == "4bf92f3577b34da6a3ce929d0e0e4736"
    assert ctx.span_id == "00f067aa0ba902b7"
    assert is_sampled(ctx)
    assert format_header(ctx) == GOOD


@pytest.mark.parametrize(
    "bad",
    [
        "",
        "00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7",
        "ff-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01",
        "00-00000000000000000000000000000000-00f067aa0ba902b7-01",
        "00-4bf92f3577b34da6a3ce929d0e0e4736-0000000000000000-01",
        "00-4bf92f3577b34da6a3ce929d0e0e473-00f067aa0ba902b7-01",
        "00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-1",
    ],
)
def test_malformed_headers_are_rejected(bad):
    with pytest.raises(InvalidTraceparent):
        parse(bad)


def test_all_zero_trace_id_is_invalid():
    with pytest.raises(InvalidTraceparent):
        parse("00-" + "0" * 32 + "-00f067aa0ba902b7-01")


@pytest.mark.parametrize(
    "bad",
    [
        "00-4BF92F3577B34DA6A3CE929D0E0E4736-00f067aa0ba902b7-01",
        "00-0x4bf92f3577b34da6a3ce929d0e0e47-00f067aa0ba902b7-01",
        "00-4bf92f3577b34da6a3ce929d0e0e4736-+0f067aa0ba902b7-01",
        "00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7- 1",
    ],
)
def test_only_lowercase_hex_digits_are_allowed(bad):
    with pytest.raises(InvalidTraceparent):
        parse(bad)


def test_version_00_rejects_extra_fields_but_future_versions_tolerate_them():
    with pytest.raises(InvalidTraceparent):
        parse(GOOD + "-extra")
    ctx = parse("01-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01-future-data")
    assert ctx.version == "01" and ctx.flags == "01"


def test_span_ids_are_zero_padded_and_never_zero():
    assert new_span_id(FakeRng(0x1A)) == "000000000000001a"
    assert new_span_id(FakeRng(0, 0, 255)) == "00000000000000ff"


def test_child_keeps_trace_and_flags_but_changes_span_and_version():
    parent = parse("01-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-00-x")
    child = child_context(parent, FakeRng(7))
    assert child.version == "00"
    assert child.trace_id == parent.trace_id and child.flags == "00"
    assert child.span_id == "0000000000000007"
    assert not is_sampled(child)


def test_edge_continues_valid_and_restarts_invalid_inbound_headers():
    ctx, continued = continue_or_start(GOOD, FakeRng(5))
    assert continued and ctx.trace_id == "4bf92f3577b34da6a3ce929d0e0e4736"
    ctx, continued = continue_or_start("garbage", FakeRng(0x1234, 9))
    assert not continued and ctx.trace_id.endswith("1234") and len(ctx.trace_id) == 32
    assert ctx.flags == "01"
