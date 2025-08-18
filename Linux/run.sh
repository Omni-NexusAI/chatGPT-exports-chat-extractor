#!/usr/bin/env bash
set -euo pipefail

# Resolve project root (one level up from this script's directory)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$PROJECT_ROOT"

# Choose a Python interpreter
if command -v python3 >/dev/null 2>&1; then
    PYTHON_BIN=python3
elif command -v python >/dev/null 2>&1; then
    PYTHON_BIN=python
else
    echo "Error: Python 3 not found. Please install Python 3.8+ and try again." >&2
    exit 1
fi

# Verify Tkinter is available for the selected Python
if ! "$PYTHON_BIN" - <<'PY' >/dev/null 2>&1; then
import sys
assert sys.version_info >= (3, 8)
import tkinter
PY
then
    echo "Error: Tkinter is not available for $($PYTHON_BIN -V 2>/dev/null)." >&2
    echo "Install Tkinter and try again. Examples:" >&2
    echo "  Debian/Ubuntu: sudo apt-get install -y python3-tk" >&2
    echo "  Fedora:        sudo dnf install -y python3-tkinter" >&2
    echo "  Arch:          sudo pacman -S tk" >&2
    exit 1
fi

# Run the GUI, forwarding any arguments (e.g., ./Linux/run.sh /path/to/chat.html)
exec "$PYTHON_BIN" chat_extractor_gui.py "$@"


