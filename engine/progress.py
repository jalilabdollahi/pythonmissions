"""Progress tracker - saves to ~/.pythonmissions/progress.json"""

from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

PROGRESS_DIR = Path.home() / ".pythonmissions"
PROGRESS_FILE = PROGRESS_DIR / "progress.json"
SCHEMA_VERSION = 2

# Total XP in the campaign: 120 x 100 + 100 x 200 + 80 x 300 = 56,000
RANKS = [
    (0, "Intern"),
    (1_000, "Junior DevOps"),
    (3_000, "DevOps Engineer"),
    (8_000, "Senior DevOps"),
    (16_000, "Staff Engineer"),
    (28_000, "Principal Engineer"),
    (45_000, "Distinguished Engineer"),
]


def _fresh(player_name: str = "") -> dict:
    return {
        "version": SCHEMA_VERSION,
        "player_name": player_name,
        "completed": {},  # mission_id -> xp awarded
        "hints_used": {},
        "solutions_viewed": [],
        "attempts": {},
    }


class Progress:
    def __init__(self, path: Path = PROGRESS_FILE):
        self.path = path
        self._data = self._load()

    def _load(self) -> dict:
        if not self.path.exists():
            return _fresh()
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return _fresh()
        if not isinstance(data, dict):
            return _fresh()
        if data.get("version") != SCHEMA_VERSION:
            # Missions were rewritten; old mission ids mean nothing now. Keep the name only.
            return _fresh(str(data.get("player_name", "")))
        fresh = _fresh()
        for key, default in fresh.items():
            if not isinstance(data.get(key), type(default)):
                data[key] = default
        return data

    def _save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        fd, tmp = tempfile.mkstemp(dir=self.path.parent, prefix=".progress-", suffix=".json")
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(self._data, f, indent=2)
        os.replace(tmp, self.path)

    # ------------------------------------------------------------ updates

    def complete_mission(self, mission_id: str, xp: int) -> bool:
        """Mark a mission complete. Returns True if it was newly completed."""
        if mission_id in self._data["completed"]:
            return False
        self._data["completed"][mission_id] = xp
        self._save()
        return True

    def use_hint(self, mission_id: str, hint_index: int) -> None:
        used = self._data["hints_used"].setdefault(mission_id, [])
        if hint_index not in used:
            used.append(hint_index)
            self._save()

    def view_solution(self, mission_id: str) -> None:
        if mission_id not in self._data["solutions_viewed"]:
            self._data["solutions_viewed"].append(mission_id)
            self._save()

    def record_attempt(self, mission_id: str) -> None:
        self._data["attempts"][mission_id] = self._data["attempts"].get(mission_id, 0) + 1
        self._save()

    def set_player_name(self, name: str) -> None:
        self._data["player_name"] = name
        self._save()

    # ------------------------------------------------------------ queries

    def player_name(self) -> str:
        return self._data.get("player_name", "")

    def is_completed(self, mission_id: str) -> bool:
        return mission_id in self._data["completed"]

    def hints_used(self, mission_id: str) -> int:
        return len(self._data["hints_used"].get(mission_id, []))

    def solutions_viewed(self) -> List[str]:
        return self._data["solutions_viewed"]

    def attempts(self, mission_id: str) -> int:
        return self._data["attempts"].get(mission_id, 0)

    def total_xp(self, valid_ids: Optional[Iterable[str]] = None) -> int:
        completed: Dict[str, int] = self._data["completed"]
        if valid_ids is None:
            return sum(completed.values())
        valid = set(valid_ids)
        return sum(xp for mid, xp in completed.items() if mid in valid)

    def completed_count(self, valid_ids: Optional[Iterable[str]] = None) -> int:
        completed = self._data["completed"]
        if valid_ids is None:
            return len(completed)
        return len(set(completed) & set(valid_ids))

    @staticmethod
    def rank_for(xp: int) -> str:
        rank = RANKS[0][1]
        for threshold, title in RANKS:
            if xp >= threshold:
                rank = title
        return rank

    @staticmethod
    def next_rank_for(xp: int) -> Tuple[Optional[str], int]:
        """Returns (next_rank_name, xp_needed) or (None, 0) at max rank."""
        for threshold, title in RANKS:
            if xp < threshold:
                return title, threshold - xp
        return None, 0
