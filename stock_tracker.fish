#!/usr/bin/env fish

# Stock Tracker TUI Launcher (Fish Shell)
# This script launches the stock tracker TUI application

set script_dir (dirname (status --current-filename))

# Check if Python 3 is available
if not command -v python3 &> /dev/null
    echo "Error: Python 3 is required but not installed."
    exit 1
end

# Run the stock tracker application
python3 "$script_dir/stock_tracker.py" $argv
