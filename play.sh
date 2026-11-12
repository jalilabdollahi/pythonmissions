#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

if ! ./venv/bin/python -c 'import rich, yaml, pytest' >/dev/null 2>&1; then
  echo "❌ The virtual environment is missing or broken. Run ./install.sh first."
  exit 1
fi

export PYTHONPATH="$(pwd)${PYTHONPATH:+:$PYTHONPATH}"
PROGRESS_FILE="${HOME}/.pythonmissions/progress.json"

case "${1:-}" in
  --reset)
    if [ ! -f "$PROGRESS_FILE" ] && [ ! -d sandbox ]; then
      echo "ℹ️  Nothing to reset."
      exit 0
    fi
    read -r -p "⚠️  Reset all progress and your sandbox edits? This cannot be undone. [y/N] " confirm
    if [[ "$confirm" =~ ^[Yy]$ ]]; then
      rm -f "$PROGRESS_FILE"
      rm -rf sandbox
      echo "✅ Progress reset. Starting again from the first mission."
    else
      echo "Cancelled."
      exit 0
    fi
    ;;
  --validate)
    shift
    exec ./venv/bin/python tools/validate_missions.py "$@"
    ;;
  "" ) ;;
  *)
    echo "Usage: ./play.sh [--reset | --validate [--only 001-020]]"
    exit 1
    ;;
esac

clear
exec ./venv/bin/python main.py
