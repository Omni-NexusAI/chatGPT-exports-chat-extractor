#!/bin/bash
set -e

# Move to project root (one level up from this script)
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR/.."

# Find Python 3
if command -v python3 >/dev/null 2>&1; then
  PY=python3
elif command -v python >/dev/null 2>&1; then
  PY=python
else
  echo "Python 3 not found. Install from python.org or via Homebrew (brew install python)."
  read -n 1 -s -r -p "Press any key to close..."
  exit 1
fi

# Check Tkinter availability
if ! "$PY" - <<'PY' >/dev/null 2>&1; then
import sys
assert sys.version_info >= (3, 8)
import tkinter
PY
then
  echo "Tkinter is not available for the current Python."
  echo "Recommend installing Python from python.org (includes Tk)."
  read -n 1 -s -r -p "Press any key to close..."
  exit 1
fi

# Run GUI and forward any dropped file args
"$PY" chat_extractor_gui.py "$@"
STATUS=$?
if [ $STATUS -ne 0 ]; then
  echo "Exited with status $STATUS"
fi
read -n 1 -s -r -p "Press any key to close..."


