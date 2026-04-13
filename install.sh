#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"

echo ""
echo "  ╔══════════════════════════════════════╗"
echo "  ║      PYTHON MISSIONS - Install       ║"
echo "  ╚══════════════════════════════════════╝"
echo ""

command -v python3 >/dev/null || { echo "❌ python3 not found"; exit 1; }
echo "  Python: $(python3 --version 2>&1)"

if [ ! -d "venv" ]; then
  echo ""
  echo "  Creating virtual environment..."
  python3 -m venv venv
fi

echo ""
echo "  Installing dependencies..."
./venv/bin/pip install -r requirements.txt --quiet

chmod +x setup.sh play.sh

echo ""
echo "  ✓ Install complete!"
echo ""
echo "  Start the game with:"
echo "    ./play.sh"
echo ""
