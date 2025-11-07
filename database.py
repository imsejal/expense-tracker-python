# database.py
"""
Database connection and schema initialization.

Uses sqlite3 and ensures schema is created when a connection is obtained.
"""

import sqlite3
from sqlite3 import Connection
from typing import Optional

DB_PATH = "expenses.db"


def get_db_connection(db_path: Optional[str] = None) -> Connection:
    """
    Return a sqlite3.Connection with row_factory set to sqlite3.Row.
    Ensures schema is created if not already present.
    """
    path = db_path or DB_PATH
    conn = sqlite3.connect(path, detect_types=sqlite3.PARSE_DECLTYPES)
    conn.row_factory = sqlite3.Row
    # ensure foreign keys
    conn.execute("PRAGMA foreign_keys = ON;")
    # create unified schema if not exists
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,           -- format YYYY-MM-DD
        category TEXT NOT NULL,
        amount REAL NOT NULL,
        user TEXT NOT NULL DEFAULT 'self'
    );

    CREATE TABLE IF NOT EXISTS budgets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        month TEXT NOT NULL,         -- format YYYY-MM
        category TEXT NOT NULL,
        amount REAL NOT NULL,
        UNIQUE(month, category)
    );

    CREATE TABLE IF NOT EXISTS groups (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE
    );

    CREATE TABLE IF NOT EXISTS group_members (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        group_id INTEGER NOT NULL,
        member TEXT NOT NULL,
        FOREIGN KEY(group_id) REFERENCES groups(id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS group_expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        group_id INTEGER NOT NULL,
        member TEXT NOT NULL,
        category TEXT NOT NULL,
        amount REAL NOT NULL,
        date TEXT NOT NULL,
        FOREIGN KEY(group_id) REFERENCES groups(id) ON DELETE CASCADE
    );
    """)
    conn.commit()
    return conn
