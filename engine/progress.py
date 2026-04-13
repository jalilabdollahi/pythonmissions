"""Progress tracker - saves to ~/.pythonmissions/progress.json"""

import json
from pathlib import Path
from typing import List

PROGRESS_DIR = Path.home() / ".pythonmissions"
PROGRESS_FILE = PROGRESS_DIR / "progress.json"

RANKS = [
    (0, "Intern"),
    (200, "Junior DevOps"),
    (500, "DevOps Engineer"),
    (1000, "Senior DevOps"),
    (1500, "Staff Engineer"),
    (2000, "Principal Engineer"),
]


class Progress:
    def __init__(self):
        self._data = self._load()

    def _load(self) -> dict:
        PROGRESS_DIR.mkdir(parents=True, exist_ok=True)
        if PROGRESS_FILE.exists():
            with open(PROGRESS_FILE, encoding="utf-8") as f:
                data = json.load(f)
                data.setdefault("player_name", "")
                data.setdefault("completed", [])
                data.setdefault("xp", 0)
                data.setdefault("hints_used", {})
                data.setdefault("solutions_viewed", [])
                data.setdefault("attempts", {})
                return data
        return {
            "player_name": "",
            "completed": [],
            "xp": 0,
            "hints_used": {},
            "solutions_viewed": [],
            "attempts": {},
        }

    def _save(self):
        with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
            json.dump(self._data, f, indent=2)

    def complete_mission(self, mission_id: str, xp: int):
        if mission_id not in self._data["completed"]:
            self._data["completed"].append(mission_id)
            self._data["xp"] += xp
            self._save()

    def use_hint(self, mission_id: str, hint_index: int):
        used = self._data["hints_used"].setdefault(mission_id, [])
        if hint_index not in used:
            used.append(hint_index)
            self._save()

    def view_solution(self, mission_id: str):
        if mission_id not in self._data["solutions_viewed"]:
            self._data["solutions_viewed"].append(mission_id)
            self._save()

    def record_attempt(self, mission_id: str):
        self._data["attempts"][mission_id] = self._data["attempts"].get(mission_id, 0) + 1
        self._save()

    def player_name(self) -> str:
        return self._data.get("player_name", "")

    def set_player_name(self, name: str):
        self._data["player_name"] = name
        self._save()

    def is_completed(self, mission_id: str) -> bool:
        return mission_id in self._data["completed"]

    def hints_used(self, mission_id: str) -> int:
        return len(self._data["hints_used"].get(mission_id, []))

    def solutions_viewed(self) -> List[str]:
        return self._data["solutions_viewed"]

    def total_xp(self) -> int:
        return self._data["xp"]

    def completed_count(self) -> int:
        return len(self._data["completed"])

    def get_rank(self) -> str:
        xp = self.total_xp()
        rank = RANKS[0][1]
        for threshold, title in RANKS:
            if xp >= threshold:
                rank = title
        return rank

    def next_rank_info(self) -> tuple:
        """Returns (next_rank_name, xp_needed) or (None, 0) if max rank."""
        xp = self.total_xp()
        for threshold, title in RANKS:
            if xp < threshold:
                return title, threshold - xp
        return None, 0
