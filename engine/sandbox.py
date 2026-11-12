"""Sandbox helpers: each mission gets its own editable copy under sandbox/<mission-id>/.

Only broken.py is the player's file. The test file is refreshed from the mission
directory before every check, so editing the tests cannot fake a pass, and the
solution is never copied into the sandbox.
"""

from __future__ import annotations

import shutil
from pathlib import Path

SANDBOX_DIRNAME = "sandbox"


def sandbox_path(base_path: Path, mission_id: str) -> Path:
    return base_path / SANDBOX_DIRNAME / mission_id


def prepare_sandbox(base_path: Path, mission_path: Path) -> Path:
    """Create the sandbox for a mission, keeping the player's earlier edits if present."""
    root = sandbox_path(base_path, mission_path.name)
    root.mkdir(parents=True, exist_ok=True)
    work_file = root / "broken.py"
    if not work_file.exists():
        shutil.copy2(mission_path / "broken.py", work_file)
    refresh_tests(root, mission_path)
    return root


def refresh_tests(root: Path, mission_path: Path) -> None:
    shutil.copy2(mission_path / "test_mission.py", root / "test_mission.py")


def reset_sandbox(root: Path, mission_path: Path) -> bool:
    """Restore broken.py in the sandbox to the mission's original broken version."""
    source = mission_path / "broken.py"
    if not source.exists():
        return False
    shutil.copy2(source, root / "broken.py")
    return True
