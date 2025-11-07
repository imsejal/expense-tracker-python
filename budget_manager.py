from database import get_db_connection
from email_alerts import send_email_alert

def set_budget(month, category, amount):
    conn = get_db_connection()
    conn.execute("""
        INSERT OR REPLACE INTO budgets (month, category, amount)
        VALUES (?, ?, ?)
    """, (month, category, amount))
    conn.commit()
    conn.close()
    print(f"💡 Budget of ₹{amount} set for '{category}' in month {month}")

def check_budget(month, category, spent, user_email=None):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT amount FROM budgets WHERE month = ? AND category = ?", (month, category))
    data = cur.fetchone()
    conn.close()
    if data:
        budget = data[0]
        remaining = budget - spent

        if spent > budget:
            msg = f"⚠️ ALERT: You exceeded your {category} budget! (Spent ₹{spent} / Budget ₹{budget})"
            print(msg)
            if user_email:
                send_email_alert(user_email, "Budget Exceeded!", msg)
        elif remaining <= 0.1 * budget:
            msg = f"🔶 Warning: Only ₹{remaining} left in your {category} budget (₹{spent}/{budget})"
            print(msg)
            if user_email:
                send_email_alert(user_email, "Budget Warning", msg)
