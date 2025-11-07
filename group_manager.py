from database import get_db_connection

def create_group(group_name, members):
    conn = get_db_connection()
    for member in members:
        conn.execute("INSERT INTO groups (group_name, member) VALUES (?, ?)", (group_name, member))
    conn.commit()
    conn.close()
    print(f"👥 Group '{group_name}' created with members: {', '.join(members)}")

def split_expense(group_name, category, amount):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT member FROM groups WHERE group_name = ?", (group_name,))
    members = [m[0] for m in cur.fetchall()]
    conn.close()

    if not members:
        print("❌ No such group found.")
        return

    share = round(amount / len(members), 2)
    print(f"💰 Each member in '{group_name}' owes ₹{share}")

    from expense_manager import add_expense
    for member in members:
        add_expense(category, share, user=member)
