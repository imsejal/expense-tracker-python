# group_manager.py
"""
Group creation and group expense splitting.

Records per-member group expenses and also records them into the
main expenses table (so personal reports include shared expenses).
"""

from database import get_db_connection
from datetime import datetime
from expense_manager import add_expense


def create_group(name: str, members: list):
    """
    Create a group with the given name and list of member names.
    Raises ValueError for invalid inputs.
    """
    if not name or not members:
        raise ValueError("Group name and members required.")

    conn = get_db_connection()
    with conn:
        cur = conn.cursor()
        # ensure group exists (INSERT OR IGNORE)
        cur.execute("INSERT OR IGNORE INTO groups (name) VALUES (?)", (name,))
        cur.execute("SELECT id FROM groups WHERE name = ?", (name,))
        gid_row = cur.fetchone()
        if not gid_row:
            raise RuntimeError("Failed to create or locate the group.")
        gid = gid_row["id"]

        # Insert members. Avoid creating duplicate identical rows.
        for m in members:
            # optional: skip blank names
            if not m:
                continue
            # Use INSERT INTO ... to allow duplicates at DB level if desired.
            cur.execute("INSERT INTO group_members (group_id, member) VALUES (?, ?)", (gid, m))


def split_expense(group_name: str, category: str, amount: float, date: str = None):
    """
    Split an expense equally among group members.

    - Records individual rows in group_expenses
    - Calls add_expense to record each member's expense in the main expenses table
    - Returns a dict with per_person and members list

    Raises ValueError for invalid inputs.
    """
    if amount <= 0:
        raise ValueError("Amount must be > 0.")
    if not group_name:
        raise ValueError("Group name is required.")
    if not category:
        raise ValueError("Category is required.")

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

    # round per-person share to 2 decimals (may cause small rounding remainder)
    share = round(amount / len(members), 2)
    dt = date or datetime.now().strftime("%Y-%m-%d")

    with conn:
        for member in members:
            conn.execute(
                "INSERT INTO group_expenses (group_id, member, category, amount, date) VALUES (?, ?, ?, ?, ?)",
                (gid, member, category, share, dt)
            )
            # also add to personal expenses table so the person's reports include it
            try:
                add_expense(category, share, user=member, date=dt)
            except Exception:
                # if personal expense add fails, continue but note it in logs (print)
                print(f"Warning: failed to add personal expense record for member '{member}'.")
    return {"per_person": share, "members": members}
