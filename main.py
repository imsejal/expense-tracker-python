import sqlite3
from datetime import datetime

# ==========================
# Database Initialization
# ==========================
def init_db():
    conn = sqlite3.connect("expenses.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        category TEXT,
        amount REAL,
        user TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS budget (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        month TEXT,
        limit_amount REAL
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS groups (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        group_name TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS group_expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        group_id INTEGER,
        member TEXT,
        amount REAL,
        FOREIGN KEY(group_id) REFERENCES groups(id)
    )
    """)

    conn.commit()
    conn.close()


# ==========================
# Expense Management
# ==========================
def add_expense(category, amount, user="self"):
    conn = sqlite3.connect("expenses.db")
    date = datetime.now().strftime("%Y-%m-%d")

    conn.execute(
        "INSERT INTO expenses (date, category, amount, user) VALUES (?, ?, ?, ?)",
        (date, category, amount, user),
    )
    conn.commit()
    conn.close()
    print(f"✅ Expense of ₹{amount} added under '{category}' for user '{user}'")


def set_budget(limit_amount):
    conn = sqlite3.connect("expenses.db")
    month = datetime.now().strftime("%Y-%m")

    conn.execute("INSERT INTO budget (month, limit_amount) VALUES (?, ?)", (month, limit_amount))
    conn.commit()
    conn.close()
    print("✅ Budget set successfully!")


def view_monthly_report():
    conn = sqlite3.connect("expenses.db")
    month = datetime.now().strftime("%Y-%m")
    cursor = conn.cursor()

    cursor.execute("SELECT category, SUM(amount) FROM expenses WHERE date LIKE ? GROUP BY category", (month + "%",))
    rows = cursor.fetchall()

    print("\n📊 Monthly Expense Report:")
    print("----------------------------")
    total = 0
    for row in rows:
        print(f"Category: {row[0]} | Amount: ₹{row[1]}")
        total += row[1]

    print("----------------------------")
    print(f"Total Spent: ₹{total}")

    cursor.execute("SELECT limit_amount FROM budget WHERE month=?", (month,))
    budget = cursor.fetchone()

    if budget:
        print(f"Budget Limit: ₹{budget[0]}")
        if total > budget[0]:
            print("⚠️ You have exceeded your budget!")
        elif total > 0.9 * budget[0]:
            print("⚠️ Alert: Only 10% budget left!")
        else:
            print("✅ You are within your budget.")
    else:
        print("No budget set for this month.")

    conn.close()


# ==========================
# Group Management (Splitwise-style)
# ==========================
def create_group(group_name):
    conn = sqlite3.connect("expenses.db")
    conn.execute("INSERT INTO groups (group_name) VALUES (?)", (group_name,))
    conn.commit()
    conn.close()
    print(f"✅ Group '{group_name}' created successfully!")


def add_group_expense(group_name, member, amount):
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM groups WHERE group_name=?", (group_name,))
    group = cursor.fetchone()

    if group:
        group_id = group[0]
        conn.execute(
            "INSERT INTO group_expenses (group_id, member, amount) VALUES (?, ?, ?)",
            (group_id, member, amount),
        )
        conn.commit()
        print(f"✅ Expense of ₹{amount} added for '{member}' in group '{group_name}'!")
    else:
        print("❌ Group not found.")
    conn.close()


# ==========================
# Main Menu
# ==========================
def main():
    init_db()
    while True:
        print("\n========= Expense Tracker =========")
        print("1. Add Expense")
        print("2. Set Budget")
        print("3. View Monthly Report")
        print("4. Create Group (Splitwise)")
        print("5. Add Group Expense")
        print("6. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            category = input("Enter category: ")
            amount = float(input("Enter amount: "))
            add_expense(category, amount)

        elif choice == "2":
            limit_amount = float(input("Enter monthly budget limit: "))
            set_budget(limit_amount)

        elif choice == "3":
            view_monthly_report()

        elif choice == "4":
            group_name = input("Enter group name: ")
            create_group(group_name)

        elif choice == "5":
            group_name = input("Enter group name: ")
            member = input("Enter member name: ")
            amount = float(input("Enter amount: "))
            add_group_expense(group_name, member, amount)

        elif choice == "6":
            print("👋 Exiting... Goodbye!")
            break

        else:
            print("❌ Invalid choice, please try again.")


if __name__ == "__main__":
    main()
