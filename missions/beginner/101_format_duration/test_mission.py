import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

from broken import format_duration, board_line


def test_minutes_and_seconds_are_not_swapped():
    assert format_duration(125).endswith("02:05"), "125s is 2 minutes 5 seconds; divmod returns (quotient, remainder)"


def test_fields_are_zero_padded():
    assert format_duration(3725) == "01:02:05"


def test_zero_is_all_zeros():
    assert format_duration(0) == "00:00:00"


def test_hours_do_not_wrap_at_24():
    assert format_duration(100 * 3600) == "100:00:00"


def test_negative_raises_value_error():
    with pytest.raises(ValueError):
        format_duration(-1)


def test_board_line_contains_host_and_clock():
    assert board_line("edge-9", 59) == "edge-9 up 00:00:59"
