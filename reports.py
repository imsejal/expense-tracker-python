# reports.py
"""
Report generation utilities.

Prints a per-category monthly expense table and total spending.
Also checks budgets and prints simple alerts.
"""
from expense_manager import get_monthly_expenses, get_total_spending
from budget_manager import check_budget_and_maybe_alert
from tabulate import tabulate

def generate_report(month: str, email: str = None):
    """
    Generate and print a monthly report for `month` (format YYYY-MM).
    If email is provided, budget alerts may be emailed as configured.
    """
    if not month or len(month) != 7:
        print("Month must be in YYYY-MM format.")
        return

    try:
        rows = get_monthly_expenses(month)
    except Exception as e:
        print(f"Error fetching expenses: {e}")
        return

    if not rows:
        print("No expenses this month.")
    else:
        table = [(r["category"], r["total"]) for r in rows]
        print("\nMonthly Expense Report")
        print(tabulate(table, headers=["Category", "Total Spent"], tablefmt="grid"))

    try:
        total = get_total_spending(month)
        print(f"\nTotal spending this month: ₹{total:.2f}")
    except Exception as e:
        print(f"Error computing total spending: {e}")
        total = 0

    # check per-category budgets and alert if needed
    for r in rows:
        try:
            res = check_budget_and_maybe_alert(month, r["category"], email=email)
            if res and res.get("status") != "ok":
                # present concise alert to user
                if res["status"] == "exceeded":
                    print(f"ALERT: Budget exceeded for '{r['category']}' (spent ₹{res['spent']} / budget ₹{res['budget']}).")
                elif res["status"] == "low":
                    print(f"WARNING: Low remaining budget for '{r['category']}' (remaining ₹{res['remaining']:.2f}).")
        except Exception as e:
            print(f"Failed to check budget for category {r['category']}: {e}")