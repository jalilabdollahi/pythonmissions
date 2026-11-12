"""Tests for the game engine (not the missions). Run: python -m pytest tests"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from engine.missions import load_missions
from engine.progress import Progress, SCHEMA_VERSION
from engine.runner import run_tests
from engine.sandbox import prepare_sandbox, reset_sandbox

GOOD_YAML = """title: Demo
category: Basics
difficulty: 1
xp: 100
story: |
  A story with [brackets] and "quotes".
description: |
  There is 1 bug.
hints:
  - |
    Use [expr for x in xs if cond].
  - two
  - three
tags: [demo]
lesson: |
  Something useful.
mistakes:
  - one
  - two
"""

BROKEN = "def add(a, b):\n    return a - b\n"
FIXED = "def add(a, b):\n    return a + b\n"
TEST = (
    "import os, sys\n"
    "sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))\n"
    "from broken import add\n\n"
    "def test_add():\n    assert add(2, 3) == 5\n"
)


def make_mission(base: Path, level: str, name: str, yaml_text: str = GOOD_YAML) -> Path:
    d = base / "missions" / level / name
    d.mkdir(parents=True)
    (d / "mission.yaml").write_text(yaml_text, encoding="utf-8")
    (d / "broken.py").write_text(BROKEN, encoding="utf-8")
    (d / "solution.py").write_text(FIXED, encoding="utf-8")
    (d / "test_mission.py").write_text(TEST, encoding="utf-8")
    return d


def test_invalid_yaml_is_skipped_not_fatal(tmp_path):
    make_mission(tmp_path, "beginner", "001_ok")
    make_mission(tmp_path, "beginner", "002_bad", 'title: x\nhints:\n  - "a "b" c"\n')
    missions, errors = load_missions(tmp_path)
    assert [m.id for m in missions] == ["001_ok"]
    assert len(errors) == 1 and "002_bad" in errors[0]


def test_missions_are_ordered_by_level_then_number(tmp_path):
    make_mission(tmp_path, "advanced", "221_c")
    make_mission(tmp_path, "beginner", "002_b")
    make_mission(tmp_path, "beginner", "001_a")
    make_mission(tmp_path, "intermediate", "121_x")
    missions, _ = load_missions(tmp_path)
    assert [m.id for m in missions] == ["001_a", "002_b", "121_x", "221_c"]
    assert missions[0].lesson == "Something useful."
    assert missions[0].mistakes == ["one", "two"]


def test_sandbox_keeps_edits_and_reset_restores(tmp_path):
    mission = make_mission(tmp_path, "beginner", "001_ok")
    box = prepare_sandbox(tmp_path, mission)
    (box / "broken.py").write_text(FIXED, encoding="utf-8")
    box = prepare_sandbox(tmp_path, mission)  # re-entering keeps the player's work
    assert (box / "broken.py").read_text() == FIXED
    assert not (box / "solution.py").exists()
    assert reset_sandbox(box, mission)
    assert (box / "broken.py").read_text() == BROKEN


def test_run_tests_pass_and_fail(tmp_path):
    mission = make_mission(tmp_path, "beginner", "001_ok")
    box = prepare_sandbox(tmp_path, mission)
    passed, _out, failed = run_tests(box)
    assert not passed and failed == ["test_add"]
    (box / "broken.py").write_text(FIXED, encoding="utf-8")
    passed, _out, failed = run_tests(box)
    assert passed and failed == []


def test_run_tests_reports_syntax_error(tmp_path):
    mission = make_mission(tmp_path, "beginner", "001_ok")
    box = prepare_sandbox(tmp_path, mission)
    (box / "broken.py").write_text("def add(a, b)\n    return a + b\n", encoding="utf-8")
    passed, out, _ = run_tests(box)
    assert not passed and "Syntax error" in out


def test_progress_xp_and_ranks(tmp_path):
    p = Progress(tmp_path / "progress.json")
    assert p.complete_mission("001_a", 100)
    assert not p.complete_mission("001_a", 100)  # no double XP
    p.complete_mission("999_gone", 300)
    assert p.total_xp(["001_a"]) == 100  # removed missions do not count
    assert Progress.rank_for(0) == "Intern"
    assert Progress.next_rank_for(0) == ("Junior DevOps", 1000)
    assert Progress.next_rank_for(10**6) == (None, 0)
    reloaded = Progress(tmp_path / "progress.json")
    assert reloaded.is_completed("001_a")


def test_old_progress_file_is_migrated_keeping_name(tmp_path):
    path = tmp_path / "progress.json"
    path.write_text(json.dumps({"player_name": "Sam", "completed": ["001_hello_devops"], "xp": 900}))
    p = Progress(path)
    assert p.player_name() == "Sam"
    assert p.total_xp() == 0
    assert p._data["version"] == SCHEMA_VERSION


def test_corrupt_progress_file_does_not_crash(tmp_path):
    path = tmp_path / "progress.json"
    path.write_text("{not json")
    assert Progress(path).total_xp() == 0
