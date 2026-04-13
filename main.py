#!/usr/bin/env python3
"""PythonMissions - Python for DevOps. Fix broken scripts, level up."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from engine.ui import GameUI


def main():
    ui = GameUI()
    ui.run()


if __name__ == "__main__":
    main()
