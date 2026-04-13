#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"
clear

if [ ! -d "venv" ]; then
  echo "❌ Virtual environment not found. Run ./install.sh first."
  exit 1
fi

if [ ! -x "venv/bin/python" ]; then
  echo "❌ Python interpreter not found in ./venv. Run ./install.sh again."
  exit 1
fi

export PYTHONPATH="$(pwd):$PYTHONPATH"

if [[ "$1" == "--reset" ]]; then
  PROGRESS_FILE="${HOME}/.pythonmissions/progress.json"
  if [ ! -f "$PROGRESS_FILE" ]; then
    echo "ℹ️  No progress file found - nothing to reset."
    exit 0
  fi

  read -r -p "⚠️  Reset all PythonMissions progress? This cannot be undone. [y/N] " confirm
  if [[ "$confirm" =~ ^[Yy]$ ]]; then
    rm -f "$PROGRESS_FILE"
    echo "✅ Progress reset. Starting again from the first mission."
  else
    echo "Cancelled."
    exit 0
  fi
fi

if [[ "$1" == "--reset-progress" ]]; then
  echo "ℹ️  PythonMissions stores progress in ~/.pythonmissions/progress.json"
  echo "    Remove that file manually if you want a full reset."
  exit 0
fi

exec ./venv/bin/python main.py
