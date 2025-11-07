# main.py
from datetime import datetime
from database import get_db_connection  # ensures db exists
from expense_manager import add_expense
from budget_manager import set_budget
from reports import generate_report
from group_manager import create_group, split_expense

def prompt_float(prompt_text):
    val = input(prompt_text)
    try:
        f = float(val)
        if f <= 0:
            raise ValueError
        return f
    except:
        print("Enter a positive number.")
        return None

def main():
    # ensure db
    get_db_connection().close()
    while True:
        print("\n========= Expense Tracker =========")
        print("1. Add Expense")
        print("2. Set Budget (month-category)")
        print("3. View Monthly Report")
        print("4. Create Group")
        print("5. Add Group Expense (split)")
        print("6. Exit")
        choice = input("Choose an option: ").strip()
        if choice == "1":
            category = input("Enter category: ").strip()
            amount = prompt_float("Enter amount: ")
            if amount and category:
                add_expense(category, amount)
                print(f"✅ Expense added: {category} ₹{amount}")
        elif choice == "2":
            month = input("Enter month (YYYY-MM): ").strip()
            category = input("Enter category: ").strip()
            amount = prompt_float("Enter monthly budget amount: ")
            if month and category and amount:
                set_budget(month, category, amount)
                print("✅ Budget set.")
        elif choice == "3":
            month = input("Enter month to view (YYYY-MM, leave blank for current): ").strip()
            if not month:
                month = datetime.now().strftime("%Y-%m")
            generate_report(month)
        elif choice == "4":
            name = input("Group name: ").strip()
            members = input("Members (comma separated): ").strip().split(",")
            members = [m.strip() for m in members if m.strip()]
            if name and members:
                create_group(name, members)
                print(f"✅ Group '{name}' created.")
        elif choice == "5":
            g = input("Group name: ").strip()
            cat = input("Category: ").strip()
            amt = prompt_float("Total amount: ")
            if g and cat and amt:
                result = split_expense(g, cat, amt)
                print(f"✅ Split: ₹{result['per_person']} per member.")
        elif choice == "6":
            print("👋 Exiting.")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
