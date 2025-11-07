from expense_manager import get_monthly_expenses, get_total_spending
from budget_manager import check_budget
from tabulate import tabulate

def generate_report(month, email=None):
    data = get_monthly_expenses(month)
    print("\n📅 Monthly Expense Report")
    print(tabulate(data, headers=["Category", "Total Spent"], tablefmt="grid"))

    total = get_total_spending(month)
    print(f"\n💵 Total Spending this month: ₹{total}")
    for category, spent in data:
        check_budget(month, category, spent, user_email=email)
