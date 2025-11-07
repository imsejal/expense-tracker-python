# expense_manager.py
from datetime import datetime
from database import get_db_connection

def add_expense(category: str, amount: float, user: str = "self", date: str = None):
    if not category or amount <= 0:
        raise ValueError("Category required and amount must be > 0.")
    date = date or datetime.now().strftime("%Y-%m-%d")
    conn = get_db_connection()
    with conn:
        conn.execute(
            "INSERT INTO expenses (date, category, amount, user) VALUES (?, ?, ?, ?)",
            (date, category, amount, user)
        )

def get_monthly_expenses(ym: str):
    """ym = 'YYYY-MM'"""
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
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT COALESCE(SUM(amount), 0) as total
        FROM expenses
        WHERE date LIKE ?
    """, (f"{ym}-%",))
    return cur.fetchone()["total"]
