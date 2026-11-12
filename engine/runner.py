"""Test runner and editor integration."""

from __future__ import annotations

import os
import shlex
import shutil
import subprocess
import sys
from pathlib import Path
from typing import List, Tuple

TEST_TIMEOUT_SECONDS = 60


def get_editor() -> str:
    """Detect the user's preferred editor."""
    editor = os.environ.get("VISUAL") or os.environ.get("EDITOR")
    if editor:
        return editor
    for candidate in ["nano", "vim", "vi", "code", "gedit", "notepad"]:
        if shutil.which(candidate):
            return candidate
    return "nano"


def open_editor(file_path: Path) -> Tuple[bool, str]:
    """Open a file in the editor. Returns (success, error_message).

    $EDITOR may contain arguments (for example "code --wait"), so it is split
    with shlex instead of being treated as a single executable name.
    """
    command = shlex.split(get_editor()) + [str(file_path)]
    try:
        result = subprocess.run(command, check=False)
    except (OSError, ValueError) as exc:
        return False, str(exc)
    if result.returncode not in (0, None):
        return False, f"editor exited with code {result.returncode}"
    return True, ""


def run_tests(sandbox: Path) -> Tuple[bool, str, List[str]]:
    """Run the mission tests inside the sandbox.

    Returns (passed, output, failed_test_names).
    """
    test_file = sandbox / "test_mission.py"
    work_file = sandbox / "broken.py"
    if not test_file.exists():
        return False, "No test_mission.py found.", []
    if not work_file.exists():
        return False, "No broken.py found.", []

    syntax = subprocess.run(
        [sys.executable, "-m", "py_compile", str(work_file)],
        capture_output=True,
        text=True,
        check=False,
    )
    if syntax.returncode != 0:
        return False, f"Syntax error:\n{syntax.stderr.strip()}", []

    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "test_mission.py", "-v", "--tb=short",
             "--no-header", "-p", "no:cacheprovider"],
            capture_output=True,
            text=True,
            cwd=str(sandbox),
            env=env,
            timeout=TEST_TIMEOUT_SECONDS,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return False, (
            f"Tests did not finish within {TEST_TIMEOUT_SECONDS}s. "
            "Look for an infinite loop or a call that waits forever."
        ), []

    output = (result.stdout + result.stderr).strip()
    failed = []
    for line in output.splitlines():
        if line.startswith(("FAILED", "ERROR")) and "::" in line:
            failed.append(line.split("::", 1)[1].split(" ")[0])
    return result.returncode == 0, output, failed
