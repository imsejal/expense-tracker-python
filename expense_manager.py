from database import get_db_connection
from datetime import datetime

def add_expense(category, amount, user="self"):
    conn = get_db_connection()
    date = datetime.now().strftime("%Y-%m-%d")
    conn.execute(
        "INSERT INTO expenses (date, category, amount, user) VALUES (?, ?, ?, ?)",
        (date, category, amount, user),
    )
    conn.commit()
    conn.close()
    print(f"✅ Expense of ₹{amount} added under '{category}' for user '{user}'")

def get_monthly_expenses(month):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT category, SUM(amount)
        FROM expenses
        WHERE strftime('%m', date) = ?
        GROUP BY category
    """, (month,))
    result = cur.fetchall()
    conn.close()
    return result

def get_total_spending(month):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT SUM(amount)
        FROM expenses
        WHERE strftime('%m', date) = ?
    """, (month,))
    total = cur.fetchone()[0]
    conn.close()
    return total or 0
