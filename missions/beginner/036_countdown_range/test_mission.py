import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import announce, countdown_messages


def test_counts_down_to_one_then_go():
    assert countdown_messages(3) == ["T-3", "T-2", "T-1", "GO"]


def test_longer_countdown_has_all_steps():
    result = countdown_messages(10)
    assert result[0] == "T-10" and result[-2] == "T-1" and len(result) == 11


def test_zero_seconds_only_says_go():
    assert countdown_messages(0) == ["GO"]


def test_announce_posts_every_message_in_order():
    posted = []
    count = announce(2, posted.append)
    assert posted == ["T-2", "T-1", "GO"]
    assert count == 3
