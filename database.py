import sqlite3

def get_db_connection():
    conn = sqlite3.connect("expenses.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            category TEXT,
            amount REAL,
            user TEXT DEFAULT 'self'
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS budgets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            month TEXT,
            category TEXT,
            amount REAL
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS groups (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            group_name TEXT,
            member TEXT
        )
    """)
    conn.commit()
    return conn
