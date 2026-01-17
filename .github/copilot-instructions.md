# Copilot Coding Agent Instructions

## Repository Overview

**Stock Ticker Tracker** - A terminal user interface (TUI) application for managing stock ticker symbols. The application allows users to add, view, edit, and delete stock ticker symbols stored in a local SQLite database.

- **Type**: Small Python TUI application (~300 lines of Python code)
- **Language**: Python 3.x
- **Dependencies**: Python standard library only (curses, sqlite3, typing)
- **Shell Support**: Bash and Fish shell launchers

## Project Structure

```
tui-example/
├── stock_tracker.py      # Main Python application (TUI + database logic)
├── stock_tracker.sh      # Bash shell launcher script
├── stock_tracker.fish    # Fish shell launcher script
├── README.md             # User documentation
├── .gitignore            # Git ignore configuration
└── .github/              # GitHub configuration
```

### Key Files

| File | Purpose |
|------|---------|
| `stock_tracker.py` | Main application with `StockDatabase` class (database operations) and `StockTrackerTUI` class (curses-based interface) |
| `stock_tracker.sh` | Bash launcher - checks Python 3 availability and runs the app |
| `stock_tracker.fish` | Fish launcher - checks Python 3 availability and runs the app |

## Build and Validation Commands

### Syntax Validation (Always run after code changes)

```bash
# Validate Python syntax (REQUIRED before committing)
python3 -m py_compile stock_tracker.py

# Validate Bash script syntax
bash -n stock_tracker.sh
```

### Running the Application

```bash
# Run directly with Python
python3 stock_tracker.py

# Run via Bash launcher
./stock_tracker.sh

# Run via Fish launcher (if fish shell is available)
./stock_tracker.fish
```

### Verification Checklist

When making changes, **always** verify:

1. `python3 -m py_compile stock_tracker.py` - Python syntax check passes
2. `bash -n stock_tracker.sh` - Bash script syntax check passes
3. `python3 -c "import curses; import sqlite3"` - Required modules are available

## Important Notes

### No External Dependencies

This project uses **only Python standard library modules**:
- `curses` - Terminal UI
- `sqlite3` - Database operations
- `typing` - Type hints

Do **not** add requirements.txt or install external packages unless explicitly requested.

### Database File

- The application creates `stocks.db` in the working directory on first run
- This file is gitignored - do not commit database files
- Database schema is auto-created by `StockDatabase.init_database()`

### Code Architecture

The Python application has two main classes:

1. **`StockDatabase`** (lines 12-78): Handles all SQLite operations
   - `init_database()` - Creates schema
   - `add_ticker()`, `get_all_tickers()`, `update_ticker()`, `delete_ticker()`

2. **`StockTrackerTUI`** (lines 81-289): Curses-based terminal interface
   - Menu navigation with arrow keys
   - CRUD operations through interactive prompts

Entry point: `main(stdscr)` function (line 292) wrapped with `curses.wrapper()`

### Shell Launcher Scripts

Both launchers follow the same pattern:
1. Check for Python 3 availability
2. Run `stock_tracker.py` with any passed arguments

When modifying shell scripts, ensure they remain compatible with their respective shells.

## Validation Before Committing

**Always run these commands from the repository root before committing changes:**

```bash
# 1. Python syntax check
python3 -m py_compile stock_tracker.py

# 2. Bash script syntax check  
bash -n stock_tracker.sh

# 3. Verify imports work
python3 -c "from stock_tracker import StockDatabase, StockTrackerTUI"
```

## Common Pitfalls

1. **Curses requires a TTY** - The TUI cannot be fully tested in non-interactive environments. Use syntax checking for validation.

2. **Terminal size** - The UI assumes a minimum terminal size of 80 columns. The `draw_header()` method uses hardcoded width of 80.

3. **Database locking** - SQLite connections use context managers (`with sqlite3.connect()`). Always follow this pattern.

4. **Type hints** - The codebase uses `typing` module hints. Maintain consistency when adding new functions.

## Files Ignored by Git

Per `.gitignore`, the following are excluded:
- `*.db`, `*.db-journal`, `*.db-wal`, `*.db-shm` - SQLite files
- `__pycache__/`, `*.py[cod]`, `*.so` - Python bytecode
- `venv/`, `env/`, `ENV/` - Virtual environments
- `.vscode/`, `.idea/` - IDE configuration

---

**Trust these instructions.** Only search or explore further if information here is incomplete or found to be incorrect during validation.
