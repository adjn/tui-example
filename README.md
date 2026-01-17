# Stock Ticker Tracker

A terminal user interface (TUI) application for managing stock ticker symbols. This application allows you to add, view, edit, and delete stock ticker symbols stored in a local SQLite database.

## Features

- **Interactive TUI**: Navigate using arrow keys and menu selections
- **Add Tickers**: Add new stock ticker symbols with optional notes
- **View Tickers**: Display all stored ticker symbols
- **Edit Tickers**: Modify existing ticker symbols and notes
- **Delete Tickers**: Remove ticker symbols from the database
- **SQLite Storage**: All data is persisted in a local SQLite database
- **Shell Support**: Compatible with both Fish and Bash shells

## Requirements

- Python 3.x (with curses support)
- Fish shell (recommended) or Bash

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/adjn/tui-example.git
   cd tui-example
   ```

2. Ensure Python 3 is installed:
   ```bash
   python3 --version
   ```

## Usage

### Using Fish Shell (Recommended)

```fish
./stock_tracker.fish
```

### Using Bash Shell

```bash
./stock_tracker.sh
```

### Running Python Directly

```bash
python3 stock_tracker.py
```

## Navigation

- **↑/↓ Arrow Keys**: Navigate menu options
- **Enter**: Select a menu option
- **q**: Quit the application

## Menu Options

1. **View All Tickers**: Display all stored ticker symbols with their IDs and notes
2. **Add New Ticker**: Add a new ticker symbol to the database
3. **Edit Ticker**: Modify an existing ticker symbol by its ID
4. **Delete Ticker**: Remove a ticker symbol from the database by its ID
5. **Exit**: Close the application

## Database

The application stores data in a SQLite database file named `stocks.db` in the same directory as the application. The database is created automatically on first run.

### Database Schema

```sql
CREATE TABLE tickers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol TEXT NOT NULL UNIQUE,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Examples

### Adding a Ticker
1. Select "Add New Ticker" from the main menu
2. Enter the ticker symbol (e.g., "AAPL")
3. Optionally add notes (e.g., "Apple Inc.")
4. Press Enter to save

### Editing a Ticker
1. Select "View All Tickers" to see the ID of the ticker you want to edit
2. Select "Edit Ticker" from the main menu
3. Enter the ticker ID
4. Enter the new symbol and notes
5. Press Enter to save changes

### Deleting a Ticker
1. Select "View All Tickers" to see the ID of the ticker you want to delete
2. Select "Delete Ticker" from the main menu
3. Enter the ticker ID
4. Confirm deletion by pressing 'y'

## Shell Compatibility Notes

- **Fish Shell**: All features fully supported
- **Bash Shell**: All features fully supported

Both shell launchers check for Python 3 availability and provide appropriate error messages if dependencies are missing.

## License

This is a demo project for educational purposes.
