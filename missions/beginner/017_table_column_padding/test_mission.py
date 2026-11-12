import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import render_row, render_table


def test_name_is_left_aligned():
    row = render_row("planner", "up", 340)
    assert row.startswith("planner     "), "names belong on the left of their column"


def test_hours_are_right_aligned():
    row = render_row("planner", "up", 340)
    assert row.endswith("   340"), "numbers belong on the right of their column"


def test_exact_row():
    assert render_row("lidar-feed", "down", 2) == "lidar-feed   down          2"


def test_every_row_has_the_same_width():
    lines = render_table([("planner", "up", 340), ("lidar-feed", "down", 2), ("x", "up", 123456)])
    assert len({len(line) for line in lines}) == 1


def test_header_comes_first():
    lines = render_table([("planner", "up", 340)])
    assert lines[0] == "SERVICE      STATE     HOURS"
    assert len(lines) == 2
