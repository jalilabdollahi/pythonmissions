import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import enabled_flags, load_flags

SAMPLE = """\
# storefront flags
NEW_CHECKOUT=on

# sale week
FREE_SHIPPING = on
GIFT_WRAP=off
# experiments below
ONE_CLICK_BUY=on
"""


def test_flags_before_first_comment_load():
    assert load_flags(SAMPLE)["NEW_CHECKOUT"] == "on"


def test_flags_after_a_comment_still_load():
    flags = load_flags(SAMPLE)
    assert "FREE_SHIPPING" in flags, "a comment line must not stop parsing"
    assert "ONE_CLICK_BUY" in flags, "lines after the last comment must be read"


def test_all_flags_counted():
    assert len(load_flags(SAMPLE)) == 4


def test_whitespace_is_stripped():
    assert load_flags("  A  =  on  ")["A"] == "on"


def test_enabled_flags_sorted():
    assert enabled_flags(load_flags(SAMPLE)) == ["FREE_SHIPPING", "NEW_CHECKOUT", "ONE_CLICK_BUY"]
