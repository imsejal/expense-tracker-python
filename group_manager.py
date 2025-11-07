# group_manager.py
from database import get_db_connection
from datetime import datetime
from expense_manager import add_expense

def create_group(name: str, members: list):
    if not name or not members:
        raise ValueError("Group name and members required.")
    conn = get_db_connection()
    with conn:
        cur = conn.cursor()
        cur.execute("INSERT OR IGNORE INTO groups (name) VALUES (?)", (name,))
        cur.execute("SELECT id FROM groups WHERE name = ?", (name,))
        gid = cur.fetchone()["id"]
        # insert members (allow duplicate checking)
        for m in members:
            conn.execute("INSERT INTO group_members (group_id, member) VALUES (?, ?)", (gid, m))

def split_expense(group_name: str, category: str, amount: float, date: str = None):
    if amount <= 0:
        raise ValueError("Amount must be > 0.")
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id FROM groups WHERE name = ?", (group_name,))
    g = cur.fetchone()
    if not g:
        raise ValueError("Group not found.")
    gid = g["id"]
    cur.execute("SELECT member FROM group_members WHERE group_id = ?", (gid,))
    members = [r["member"] for r in cur.fetchall()]
    if not members:
        raise ValueError("Group has no members.")
    share = round(amount / len(members), 2)
    # record in group_expenses and also add to personal expenses
    dt = date or datetime.now().strftime("%Y-%m-%d")
    with conn:
        for member in members:
            conn.execute(
                "INSERT INTO group_expenses (group_id, member, category, amount, date) VALUES (?, ?, ?, ?, ?)",
                (gid, member, category, share, dt)
            )
            # add to personal expenses table as well
            add_expense(category, share, user=member, date=dt)
    return {"per_person": share, "members": members}
