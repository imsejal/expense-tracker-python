# expense_manager.py
"""
Expense storage and query helpers.
"""

from datetime import datetime
from database import get_db_connection


def add_expense(category: str, amount: float, user: str = "self", date: str = None):
    """
    Add a single expense entry.

    Parameters:
    - category (str): non-empty category name
    - amount (float): > 0
    - user (str): owner of expense
    - date (str): optional YYYY-MM-DD, if omitted uses today
    """
    if not category:
        raise ValueError("Category is required.")
    if amount is None or amount <= 0:
        raise ValueError("Amount must be > 0.")
    # basic date format validation; if not provided, use today's date
    date = date or datetime.now().strftime("%Y-%m-%d")
    # validate date format more strictly here

    conn = get_db_connection()
    with conn:
        conn.execute(
            "INSERT INTO expenses (date, category, amount, user) VALUES (?, ?, ?, ?)",
            (date, category, amount, user)
        )


def get_monthly_expenses(ym: str):
    """
    Return list of rows (sqlite3.Row) with keys: category, total
    ym must be 'YYYY-MM'
    """
    if not ym or len(ym) != 7:
        raise ValueError("Month must be in YYYY-MM format.")
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT category, SUM(amount) as total
        FROM expenses
        WHERE date LIKE ?
        GROUP BY category
    """, (f"{ym}-%",))
    return cur.fetchall()


def get_total_spending(ym: str):
    """Return numeric total spent in month ym (YYYY-MM)."""
    if not ym or len(ym) != 7:
        raise ValueError("Month must be in YYYY-MM format.")
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT COALESCE(SUM(amount), 0) as total
        FROM expenses
        WHERE date LIKE ?
    """, (f"{ym}-%",))
    return cur.fetchone()["total"]
