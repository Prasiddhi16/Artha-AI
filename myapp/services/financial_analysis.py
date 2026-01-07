from django.db.models import Sum
from myapp.models import Income, Expense,Goal,GoalContribution
from datetime import date
from decimal import Decimal

def get_user_financial_snapshot(user):
    total_income = Income.objects.filter(user=user).aggregate(
        total=Sum("amount")
    )["total"] or 0

    total_expense = Expense.objects.filter(user=user).aggregate(
        total=Sum("amount")
    )["total"] or 0
    saving_capacity = max(total_income * Decimal('0.3'), Decimal('0'))

    return {
        "income": float(total_income),
        "expense": float(total_expense),
        "saving_capacity": float(saving_capacity),
    }


def get_missed_deadline_goal(goals):
    today = date.today()
    for goal in goals:
        if goal.target_date and goal.target_date < today and goal.progress_percent < 100:
            return goal
    return None
