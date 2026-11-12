import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import broken


def test_zero_failures_is_up():
    assert broken.badge(0) == "UP"


def test_long_streak_is_down():
    assert broken.badge(5) == "DOWN"


def test_threshold_boundary_is_down():
    assert broken.badge(3) == "DOWN"
    assert broken.badge(2) == "UP"


def test_custom_threshold():
    assert broken.badge(1, threshold=1) == "DOWN"


def test_board_maps_every_service():
    assert broken.board({"radar": 0, "tower": 4}) == {"radar": "UP", "tower": "DOWN"}


def test_down_services_sorted():
    assert broken.down_services({"b": 9, "a": 3, "c": 0}) == ["a", "b"]


def test_render_lines():
    assert broken.render({"tower": 4, "radar": 1}) == "radar: UP\ntower: DOWN"
