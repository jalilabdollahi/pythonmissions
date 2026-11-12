#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

echo ""
echo "  ╔══════════════════════════════════════╗"
echo "  ║      PYTHON MISSIONS - Install       ║"
echo "  ╚══════════════════════════════════════╝"
echo ""

PYTHON="${PYTHON:-python3}"
command -v "$PYTHON" >/dev/null || { echo "❌ $PYTHON not found. Install Python 3.10 or newer."; exit 1; }

if ! "$PYTHON" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)'; then
  echo "❌ Python 3.10+ is required (found $("$PYTHON" --version 2>&1))."
  echo "   Set PYTHON=/path/to/python3.x and run ./install.sh again."
  exit 1
fi
echo "  Python: $("$PYTHON" --version 2>&1)"

# A venv copied from another machine (or built by a Python that was later
# removed) has dangling interpreter links. Detect that and rebuild it.
if [ -d "venv" ] && ! ./venv/bin/python -c 'import sys' >/dev/null 2>&1; then
  echo ""
  echo "  Existing venv is broken - rebuilding it..."
  rm -rf venv
fi

if [ ! -d "venv" ]; then
  echo ""
  echo "  Creating virtual environment..."
  "$PYTHON" -m venv venv
fi

echo ""
echo "  Installing dependencies..."
./venv/bin/python -m pip install --quiet --upgrade pip
./venv/bin/python -m pip install --quiet -r requirements.txt

chmod +x play.sh

echo ""
echo "  ✓ Install complete!"
echo ""
echo "  Start the game with:"
echo "    ./play.sh"
echo ""
