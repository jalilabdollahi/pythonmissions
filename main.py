#!/usr/bin/env python3
"""PythonMissions - Python for DevOps. Fix broken scripts, level up."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from engine.ui import GameUI


def main() -> int:
    ui = GameUI()
    try:
        ui.run()
    except (KeyboardInterrupt, EOFError):
        print("\n\nGoodbye! Your progress and sandbox edits are saved.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
