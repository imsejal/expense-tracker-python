# main.py 
""" Here is The CLI point for Expense Tracker.
It provides simple menu for:
- adding expenses
- setting budgets
- viewing reports
- creating groups and splitting expenses
"""
from datetime import datetime
from database import get_db_connection  # ensures db exists
from expense_manager import add_expense
from budget_manager import set_budget
from reports import generate_report
from group_manager import create_group, split_expense


def prompt_float(prompt_text):
    """
    Prompt the user for a positive float. Returns float or None on invalid input.
    """
    val = input(prompt_text).strip()
    try:
        f = float(val)
        if f <= 0:
            print("Please enter a positive number.")
            return None
        return f
    except ValueError:
        print("Invalid number. Please enter digits only (e.g. 150.50).")
        return None
    
def safe_input(prompt_text):
    """Wrapper around input to catch KeyboardInterrupt and EOFError."""
    try:
        return input(prompt_text)
    except (KeyboardInterrupt, EOFError):
        print("\nInput interrupted. Returning to menu.")
        return ""


def main():
     # ensure DB and schema exist
    conn = get_db_connection()
    conn.close()

    while True:
        print("\n========= Expense Tracker =========")
        print("1. Add Expense")
        print("2. Set Budget (month-category)")
        print("3. View Monthly Report")
        print("4. Create Group")
        print("5. Add Group Expense (split)")
        print("6. Exit")
        choice = safe_input("Choose an option: ").strip()
        if choice == "1":
            category = safe_input("Enter category: ").strip()
            amount = prompt_float("Enter amount: ")
            if amount is None:
                continue
            if not category:
                print("Category cannot be empty.")
                continue
            try:
                add_expense(category, amount)
                print(f"Expense added: {category} ₹{amount:.2f}")
            except Exception as e:
                print(f"Failed to add expense: {e}")

        elif choice == "2":
            month = safe_input("Enter month (YYYY-MM): ").strip()
            category = safe_input("Enter category: ").strip()
            amount = prompt_float("Enter monthly budget amount: ")
            if amount is None:
                continue
            if not month or not category:
                print("Month and category are required.")
                continue
            try:
                set_budget(month, category, amount)
                print("Budget set.")
            except Exception as e:
                print(f"Failed to set budget: {e}")

        elif choice == "3":
            month = safe_input("Enter month to view (YYYY-MM, leave blank for current): ").strip()
            if not month:
                month = datetime.now().strftime("%Y-%m")
            try:
                generate_report(month)
            except Exception as e:
                print(f"Failed to generate report: {e}")

        elif choice == "4":
            name = safe_input("Group name: ").strip()
            members_input = safe_input("Members (comma separated): ").strip()
            members = [m.strip() for m in members_input.split(",") if m.strip()]
            if not name or not members:
                print("Group name and at least one member are required.")
                continue
            try:
                create_group(name, members)
                print(f"Group '{name}' created with members: {', '.join(members)}")
            except Exception as e:
                print(f"Failed to create group: {e}")

        elif choice == "5":
            g = safe_input("Group name: ").strip()
            cat = safe_input("Category: ").strip()
            amt = prompt_float("Total amount: ")
            if amt is None:
                continue
            if not g or not cat:
                print("Group name and category are required.")
                continue
            try:
                result = split_expense(g, cat, amt)
                print(f"Split: ₹{result['per_person']:.2f} per member.")
                print("Members:", ", ".join(result["members"]))
            except Exception as e:
                print(f"Failed to split expense: {e}")

        elif choice == "6":
            print("Exiting.")
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        # Top-level guard to ensure any unexpected crash prints an explanatory message.
        print(f"An unexpected error occurred: {e}")