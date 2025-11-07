# reports.py
from expense_manager import get_monthly_expenses, get_total_spending
from budget_manager import check_budget_and_maybe_alert
from tabulate import tabulate

def generate_report(month: str, email: str = None):
    rows = get_monthly_expenses(month)
    if not rows:
        print("No expenses this month.")
    else:
        table = [(r["category"], r["total"]) for r in rows]
        print("\n📅 Monthly Expense Report")
        print(tabulate(table, headers=["Category", "Total Spent"], tablefmt="grid"))
    total = get_total_spending(month)
    print(f"\n💵 Total Spending this month: ₹{total:.2f}")
    # check per-category budgets and alert if needed
    for r in rows:
        res = check_budget_and_maybe_alert(month, r["category"], email=email)
        if res and res["status"] != "ok":
            print(res)
