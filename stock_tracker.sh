#!/usr/bin/env bash

# Stock Tracker TUI Launcher (Bash Shell)
# This script launches the stock tracker TUI application

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not installed."
    exit 1
fi

# Run the stock tracker application
python3 "$SCRIPT_DIR/stock_tracker.py" "$@"
