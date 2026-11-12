import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

from broken import allocate, first_free_port


def test_returns_start_when_nothing_is_used():
    assert first_free_port(8000, 8005, []) == 8000


def test_skips_busy_ports():
    assert first_free_port(8000, 8005, [8000, 8001, 8003]) == 8002, "must return the lowest FREE port"


def test_last_port_in_range_is_usable():
    busy = list(range(8000, 8005))
    assert first_free_port(8000, 8005, busy) == 8005, "the range end is inclusive"


def test_raises_when_range_is_full():
    with pytest.raises(RuntimeError, match="no free port"):
        first_free_port(8000, 8002, [8000, 8001, 8002])


def test_single_port_range():
    assert first_free_port(9000, 9000, []) == 9000


def test_allocate_marks_port_as_used():
    port, used = allocate(8000, 8003, {8000})
    assert port == 8001
    assert used == {8000, 8001}
