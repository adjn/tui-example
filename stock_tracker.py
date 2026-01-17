#!/usr/bin/env python3
"""
Stock Ticker TUI Application
A terminal user interface for managing stock ticker symbols stored in SQLite.
"""

import argparse
import curses
import sqlite3
from typing import List, Tuple, Optional

VERSION = "1.0.0"


class StockDatabase:
    """Handles all database operations for stock ticker symbols."""
    
    def __init__(self, db_path: str = "stocks.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the database with the required schema."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tickers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    symbol TEXT NOT NULL UNIQUE,
                    notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
    
    def add_ticker(self, symbol: str, notes: str = "") -> bool:
        """Add a new ticker symbol to the database."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO tickers (symbol, notes) VALUES (?, ?)",
                    (symbol.upper(), notes)
                )
                conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
    
    def get_all_tickers(self) -> List[Tuple[int, str, str]]:
        """Retrieve all ticker symbols from the database."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, symbol, notes FROM tickers ORDER BY symbol")
            tickers = cursor.fetchall()
        return tickers
    
    def update_ticker(self, ticker_id: int, symbol: str, notes: str) -> bool:
        """Update an existing ticker symbol."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE tickers SET symbol = ?, notes = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                    (symbol.upper(), notes, ticker_id)
                )
                rowcount = cursor.rowcount
                conn.commit()
            return rowcount > 0
        except sqlite3.IntegrityError:
            return False
    
    def delete_ticker(self, ticker_id: int) -> bool:
        """Delete a ticker symbol from the database."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM tickers WHERE id = ?", (ticker_id,))
            conn.commit()
            success = cursor.rowcount > 0
        return success


class StockTrackerTUI:
    """Terminal User Interface for the Stock Tracker application."""
    
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.db = StockDatabase()
        self.current_row = 0
        self.menu_items = [
            "View All Tickers",
            "Add New Ticker",
            "Edit Ticker",
            "Delete Ticker",
            "Exit"
        ]
        
        # Setup colors
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLACK)
        
        curses.curs_set(0)  # Hide cursor
    
    def draw_header(self):
        """Draw the application header."""
        self.stdscr.addstr(0, 0, "=" * 80)
        title = "Stock Ticker Tracker"
        self.stdscr.addstr(1, (80 - len(title)) // 2, title, curses.color_pair(2) | curses.A_BOLD)
        self.stdscr.addstr(2, 0, "=" * 80)
    
    def draw_menu(self):
        """Draw the main menu."""
        self.stdscr.clear()
        self.draw_header()
        
        self.stdscr.addstr(4, 2, "Main Menu:", curses.A_BOLD)
        
        for idx, item in enumerate(self.menu_items):
            y = 6 + idx
            if idx == self.current_row:
                self.stdscr.addstr(y, 4, f"> {item}", curses.color_pair(1))
            else:
                self.stdscr.addstr(y, 4, f"  {item}")
        
        self.stdscr.addstr(len(self.menu_items) + 8, 2, "Use ↑/↓ arrows to navigate, Enter to select, 'q' to quit")
        self.stdscr.refresh()
    
    def get_input(self, prompt: str, y: int, x: int = 2) -> Optional[str]:
        """Get user input with a prompt."""
        curses.echo()
        curses.curs_set(1)
        self.stdscr.addstr(y, x, prompt)
        self.stdscr.refresh()
        
        input_str = self.stdscr.getstr(y, x + len(prompt), 40).decode('utf-8')
        
        curses.noecho()
        curses.curs_set(0)
        return input_str.strip()
    
    def show_message(self, message: str, color_pair: int = 0):
        """Display a message and wait for user to press a key."""
        height, width = self.stdscr.getmaxyx()
        self.stdscr.addstr(height - 2, 2, message, curses.color_pair(color_pair))
        self.stdscr.addstr(height - 1, 2, "Press any key to continue...")
        self.stdscr.refresh()
        self.stdscr.getch()
    
    def view_all_tickers(self):
        """Display all ticker symbols."""
        self.stdscr.clear()
        self.draw_header()
        
        tickers = self.db.get_all_tickers()
        
        if not tickers:
            self.stdscr.addstr(4, 2, "No tickers found in the database.", curses.color_pair(3))
        else:
            self.stdscr.addstr(4, 2, f"Total Tickers: {len(tickers)}", curses.A_BOLD)
            self.stdscr.addstr(6, 2, "ID", curses.A_BOLD)
            self.stdscr.addstr(6, 8, "Symbol", curses.A_BOLD)
            self.stdscr.addstr(6, 20, "Notes", curses.A_BOLD)
            self.stdscr.addstr(7, 2, "-" * 76)
            
            for idx, (ticker_id, symbol, notes) in enumerate(tickers[:20]):  # Limit to 20 rows
                y = 8 + idx
                self.stdscr.addstr(y, 2, str(ticker_id))
                self.stdscr.addstr(y, 8, symbol, curses.color_pair(4))
                notes_display = (notes or "")[:50]  # Truncate notes
                self.stdscr.addstr(y, 20, notes_display)
        
        self.show_message("")
    
    def add_ticker(self):
        """Add a new ticker symbol."""
        self.stdscr.clear()
        self.draw_header()
        
        self.stdscr.addstr(4, 2, "Add New Ticker", curses.A_BOLD)
        
        symbol = self.get_input("Ticker Symbol: ", 6)
        if not symbol:
            self.show_message("Operation cancelled.", 3)
            return
        
        notes = self.get_input("Notes (optional): ", 7)
        
        if self.db.add_ticker(symbol, notes):
            self.show_message(f"Ticker '{symbol.upper()}' added successfully!", 2)
        else:
            self.show_message(f"Error: Ticker '{symbol.upper()}' already exists!", 3)
    
    def edit_ticker(self):
        """Edit an existing ticker symbol."""
        self.stdscr.clear()
        self.draw_header()
        
        self.stdscr.addstr(4, 2, "Edit Ticker", curses.A_BOLD)
        
        ticker_id_str = self.get_input("Enter Ticker ID to edit: ", 6)
        if not ticker_id_str:
            self.show_message("Operation cancelled.", 3)
            return
        
        try:
            ticker_id = int(ticker_id_str)
        except ValueError:
            self.show_message("Invalid ID. Must be a number.", 3)
            return
        
        # Check if ticker exists
        tickers = self.db.get_all_tickers()
        ticker_data = next((t for t in tickers if t[0] == ticker_id), None)
        
        if not ticker_data:
            self.show_message(f"Ticker with ID {ticker_id} not found.", 3)
            return
        
        _, old_symbol, old_notes = ticker_data
        self.stdscr.addstr(8, 2, f"Current: {old_symbol} - {old_notes}", curses.color_pair(4))
        
        new_symbol = self.get_input("New Symbol: ", 10)
        if not new_symbol:
            new_symbol = old_symbol
        
        new_notes = self.get_input("New Notes: ", 11)
        if not new_notes:
            new_notes = old_notes
        
        if self.db.update_ticker(ticker_id, new_symbol, new_notes):
            self.show_message(f"Ticker updated successfully!", 2)
        else:
            self.show_message(f"Error updating ticker. Symbol may already exist.", 3)
    
    def delete_ticker(self):
        """Delete a ticker symbol."""
        self.stdscr.clear()
        self.draw_header()
        
        self.stdscr.addstr(4, 2, "Delete Ticker", curses.A_BOLD)
        
        ticker_id_str = self.get_input("Enter Ticker ID to delete: ", 6)
        if not ticker_id_str:
            self.show_message("Operation cancelled.", 3)
            return
        
        try:
            ticker_id = int(ticker_id_str)
        except ValueError:
            self.show_message("Invalid ID. Must be a number.", 3)
            return
        
        # Confirm deletion
        self.stdscr.addstr(8, 2, "Are you sure? (y/n): ")
        self.stdscr.refresh()
        confirm = self.stdscr.getch()
        
        if chr(confirm).lower() == 'y':
            if self.db.delete_ticker(ticker_id):
                self.show_message(f"Ticker deleted successfully!", 2)
            else:
                self.show_message(f"Ticker with ID {ticker_id} not found.", 3)
        else:
            self.show_message("Deletion cancelled.", 3)
    
    def run(self):
        """Main application loop."""
        while True:
            self.draw_menu()
            
            key = self.stdscr.getch()
            
            if key == curses.KEY_UP and self.current_row > 0:
                self.current_row -= 1
            elif key == curses.KEY_DOWN and self.current_row < len(self.menu_items) - 1:
                self.current_row += 1
            elif key == ord('\n'):  # Enter key
                if self.current_row == 0:
                    self.view_all_tickers()
                elif self.current_row == 1:
                    self.add_ticker()
                elif self.current_row == 2:
                    self.edit_ticker()
                elif self.current_row == 3:
                    self.delete_ticker()
                elif self.current_row == 4:
                    break
            elif key == ord('q') or key == ord('Q'):
                break


def main(stdscr):
    """Entry point for the curses application."""
    app = StockTrackerTUI(stdscr)
    app.run()


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        prog="stock_tracker",
        description="Stock Ticker TUI Application - A terminal user interface for managing stock ticker symbols stored in SQLite.",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "-v", "--version",
        action="version",
        version=f"%(prog)s {VERSION}",
        help="Show the version number and exit"
    )
    return parser.parse_args()


if __name__ == "__main__":
    parse_args()
    curses.wrapper(main)
