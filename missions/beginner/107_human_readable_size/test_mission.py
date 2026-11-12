import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

from broken import human_size, largest_volume, total_size


def test_plain_bytes_are_integers():
    assert human_size(512) == "512 B"


def test_exactly_one_kibibyte_is_1_0_kib():
    assert human_size(1024) == "1.0 KiB", "a value equal to the threshold already belongs to the next unit"


def test_one_and_a_half_kib():
    assert human_size(1536) == "1.5 KiB"


def test_binary_steps_not_decimal():
    assert human_size(1_000_000) == "976.6 KiB", "each step divides by 1024"


def test_gibibytes_and_exact_mebibyte():
    assert human_size(5 * 1024 ** 3) == "5.0 GiB"
    assert human_size(1024 ** 2) == "1.0 MiB"


def test_huge_values_stop_at_tib():
    assert human_size(2048 * 1024 ** 4) == "2048.0 TiB"


def test_negative_raises():
    with pytest.raises(ValueError):
        human_size(-5)


def test_largest_volume_and_total():
    vols = {"a": 2048, "b": 100}
    assert largest_volume(vols) == "a: 2.0 KiB"
    assert total_size(vols) == "2.1 KiB"
