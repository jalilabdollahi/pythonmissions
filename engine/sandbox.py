"""Sandbox helpers for editable mission copies."""

from pathlib import Path
import shutil


SANDBOX_DIRNAME = "sandbox"


def sandbox_root(base_path: Path) -> Path:
    return base_path / SANDBOX_DIRNAME / "current"


def prepare_sandbox(base_path: Path, mission_path: Path) -> Path:
    """Create a fresh editable copy of the mission under sandbox/current."""
    root = sandbox_root(base_path)
    if root.exists():
        shutil.rmtree(root)
    root.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(mission_path, root)
    return root
