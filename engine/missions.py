"""Mission loader - reads mission.yaml files from the missions/ directory."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Tuple

import yaml

LEVELS = ["beginner", "intermediate", "advanced"]


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
    lesson: str = ""
    mistakes: List[str] = field(default_factory=list)

    @property
    def number(self) -> str:
        return self.id.split("_", 1)[0]

    @property
    def broken_path(self) -> Path:
        return self.path / "broken.py"

    @property
    def test_path(self) -> Path:
        return self.path / "test_mission.py"

    @property
    def solution_path(self) -> Path:
        return self.path / "solution.py"

    @property
    def difficulty_stars(self) -> str:
        d = max(0, min(5, self.difficulty))
        return "★" * d + "☆" * (5 - d)


def _as_str_list(value) -> List[str]:
    if not isinstance(value, list):
        return []
    return [str(v).strip() for v in value if str(v).strip()]


def load_missions(base_path: Path) -> Tuple[List[Mission], List[str]]:
    """Scan missions/ and return (missions sorted by level then number, load_errors).

    A broken mission.yaml never stops the game: the mission is skipped and the
    problem is reported in load_errors.
    """
    missions: List[Mission] = []
    errors: List[str] = []
    missions_dir = base_path / "missions"

    for level in LEVELS:
        level_dir = missions_dir / level
        if not level_dir.exists():
            continue
        for mission_dir in sorted(level_dir.iterdir(), key=lambda p: p.name):
            yaml_path = mission_dir / "mission.yaml"
            if not mission_dir.is_dir() or not yaml_path.exists():
                continue
            try:
                data = yaml.safe_load(yaml_path.read_text(encoding="utf-8"))
                if not isinstance(data, dict) or not data.get("title"):
                    raise ValueError("mission.yaml must be a mapping with a title")
                if not (mission_dir / "broken.py").exists() or not (mission_dir / "test_mission.py").exists():
                    raise ValueError("broken.py or test_mission.py is missing")
                missions.append(
                    Mission(
                        id=mission_dir.name,
                        title=str(data["title"]).strip(),
                        level=level,
                        category=str(data.get("category", "General")),
                        difficulty=int(data.get("difficulty", 1)),
                        xp=int(data.get("xp", 100)),
                        description=str(data.get("description", "")).strip(),
                        story=str(data.get("story", "")).strip(),
                        hints=_as_str_list(data.get("hints")),
                        tags=_as_str_list(data.get("tags")),
                        path=mission_dir,
                        lesson=str(data.get("lesson", "")).strip(),
                        mistakes=_as_str_list(data.get("mistakes")),
                    )
                )
            except (yaml.YAMLError, ValueError, TypeError) as exc:
                first_line = str(exc).splitlines()[0] if str(exc) else type(exc).__name__
                errors.append(f"{level}/{mission_dir.name}: {first_line}")
    return missions, errors
