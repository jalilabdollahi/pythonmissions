"""Mission loader - reads mission.yaml files from missions/ directory."""

from dataclasses import dataclass
from pathlib import Path
from typing import List

import yaml


@dataclass
class Mission:
    id: str
    title: str
    level: str
    category: str
    difficulty: int
    xp: int
    description: str
    story: str
    hints: List[str]
    tags: List[str]
    path: Path

    @property
    def broken_path(self) -> Path:
        return self.path / "broken.py"

    @property
    def original_path(self) -> Path:
        return self.path / "original.py"

    @property
    def test_path(self) -> Path:
        return self.path / "test_mission.py"

    @property
    def solution_path(self) -> Path:
        return self.path / "solution.py"

    @property
    def difficulty_stars(self) -> str:
        return "★" * self.difficulty + "☆" * (5 - self.difficulty)

    @property
    def level_color(self) -> str:
        return {
            "beginner": "green",
            "intermediate": "yellow",
            "advanced": "red",
        }.get(self.level, "white")


def load_missions(base_path: Path) -> List[Mission]:
    """Scan missions/ directory and return sorted list of Mission objects."""
    missions = []
    missions_dir = base_path / "missions"
    levels = ["beginner", "intermediate", "advanced"]

    for level in levels:
        level_dir = missions_dir / level
        if not level_dir.exists():
            continue
        for mission_dir in sorted(level_dir.iterdir()):
            if not mission_dir.is_dir():
                continue
            yaml_path = mission_dir / "mission.yaml"
            if not yaml_path.exists():
                continue
            with open(yaml_path, encoding="utf-8") as f:
                data = yaml.safe_load(f)
            missions.append(
                Mission(
                    id=mission_dir.name,
                    title=data["title"],
                    level=level,
                    category=data.get("category", "General"),
                    difficulty=data.get("difficulty", 1),
                    xp=data.get("xp", 100),
                    description=data.get("description", ""),
                    story=data.get("story", ""),
                    hints=data.get("hints", []),
                    tags=data.get("tags", []),
                    path=mission_dir,
                )
            )
    return missions
