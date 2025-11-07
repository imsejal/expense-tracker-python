# budget_manager.py
from database import get_db_connection
from expense_manager import get_monthly_expenses
from email_alerts import send_email_alert

def set_budget(month: str, category: str, amount: float):
    if amount <= 0:
        raise ValueError("Budget amount must be > 0.")
    conn = get_db_connection()
    with conn:
        conn.execute("""
            INSERT INTO budgets (month, category, amount)
            VALUES (?, ?, ?)
            ON CONFLICT(month, category) DO UPDATE SET amount=excluded.amount
        """, (month, category, amount))

def check_budget_and_maybe_alert(month: str, category: str, email: str = None):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT amount FROM budgets WHERE month = ? AND category = ?", (month, category))
    row = cur.fetchone()
    if not row:
        return None
    budget = row["amount"]
    # compute spent
    cur.execute("""
        SELECT COALESCE(SUM(amount),0) AS spent
        FROM expenses
        WHERE date LIKE ? AND category = ?
    """, (f"{month}-%", category))
    spent = cur.fetchone()["spent"]
    remaining = budget - spent
    # alerts
    if spent > budget:
        msg = f"⚠️ You exceeded {category} budget for {month}! Spent ₹{spent} / Budget ₹{budget}"
        if email:
            send_email_alert(email, "Budget Exceeded", msg)
        return {"status": "exceeded", "spent": spent, "budget": budget}
    elif remaining <= 0.1 * budget:
        msg = f"🔶 Only ₹{remaining:.2f} left for {category} in {month} (₹{spent}/{budget})"
        if email:
            send_email_alert(email, "Budget Warning", msg)
        return {"status": "low", "remaining": remaining, "spent": spent, "budget": budget}
    return {"status": "ok", "remaining": remaining, "spent": spent, "budget": budget}
