"""Test runner and editor integration."""

import shutil
import subprocess
import sys
from pathlib import Path
from typing import List, Tuple


def get_editor() -> str:
    """Detect user's preferred editor."""
    import os

    editor = os.environ.get("EDITOR") or os.environ.get("VISUAL")
    if editor:
        return editor
    for ed in ["nano", "vim", "vi", "code", "gedit", "notepad"]:
        if shutil.which(ed):
            return ed
    return "nano"


def open_editor(file_path: Path) -> Tuple[bool, str]:
    """Open file in editor. Returns (success, error_message)."""
    editor = get_editor()
    try:
        subprocess.run([editor, str(file_path)], check=False)
        return True, ""
    except Exception as e:
        return False, str(e)


def run_tests(mission_path: Path) -> Tuple[bool, str, List[str]]:
    """
    Run tests for a mission.
    Returns: (passed, human_readable_output, list_of_failed_test_names)
    """
    test_file = mission_path / "test_mission.py"
    broken_file = mission_path / "broken.py"

    if not test_file.exists():
        return False, "No test_mission.py found.", []
    if not broken_file.exists():
        return False, "No broken.py found.", []

    syntax = subprocess.run(
        [sys.executable, "-m", "py_compile", str(broken_file)],
        capture_output=True,
        text=True,
        check=False,
    )
    if syntax.returncode != 0:
        return False, f"Syntax error:\n{syntax.stderr.strip()}", []

    result = subprocess.run(
        [sys.executable, "-m", "pytest", str(test_file), "-v", "--tb=short", "--no-header", "-q"],
        capture_output=True,
        text=True,
        cwd=str(mission_path),
        check=False,
    )
    output = result.stdout + result.stderr
    passed = result.returncode == 0

    failed = []
    for line in output.splitlines():
        if "FAILED" in line and "::" in line:
            name = line.strip().split("::")[-1].split(" ")[0]
            failed.append(name)

    return passed, output.strip(), failed


def reset_mission(mission_path: Path) -> bool:
    """Restore broken.py from original.py."""
    original = mission_path / "original.py"
    broken = mission_path / "broken.py"
    if not original.exists():
        return False
    shutil.copy2(original, broken)
    return True
