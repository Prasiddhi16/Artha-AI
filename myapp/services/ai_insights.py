import pandas as pd
import calendar
from datetime import datetime

def generate_ai_insights(transactions):
    """
    transactions = list of objects having:
    amount, category, transaction_type, date
    """

    data = []
    for t in transactions:
        data.append({
            "amount": float(t.amount),
            "category": t.category,
            "type": t.transaction_type,
            "date": t.date
        })

    if not data:
        return {
            "monthly_forecast": {
                "current_spent": 0,
                "projected_total": 0,
                "avg_daily": 0,
                "days_remaining": 0
            },
            "spending_trend": {
                "trend": "Stable",
                "percentage": 0
            },
            "top_category": {
                "name": "N/A",
                "amount": 0,
                "percentage": 0
            },
            "savings_rate": 0,
            "category_breakdown": []
        }

    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'])

    insights = {}
    now = datetime.now()

    # ================= MONTHLY FORECAST =================
    expense_df = df[df['type'] == 'Expense']

    month_df = expense_df[
        (expense_df['date'].dt.month == now.month) &
        (expense_df['date'].dt.year == now.year)
    ]

    total_spent = month_df['amount'].sum()
    days_passed = max(now.day, 1)
    avg_daily = total_spent / days_passed

    days_in_month = calendar.monthrange(now.year, now.month)[1]
    projected_month = avg_daily * days_in_month

    insights['monthly_forecast'] = {
        "current_spent": round(total_spent, 2),
        "avg_daily": round(avg_daily, 2),
        "projected_total": round(projected_month, 2),
        "days_remaining": days_in_month - now.day
    }

    # ================= SPENDING TREND =================
    last_month = now.month - 1 if now.month > 1 else 12

    current_total = expense_df[
        expense_df['date'].dt.month == now.month
    ]['amount'].sum()

    prev_total = expense_df[
        expense_df['date'].dt.month == last_month
    ]['amount'].sum()

    if prev_total > 0:
        change = ((current_total - prev_total) / prev_total) * 100
        trend = "Increased" if change > 0 else "Decreased"
    else:
        change = 0
        trend = "Stable"

    insights['spending_trend'] = {
        "trend": trend,
        "percentage": round(abs(change), 1)
    }

    # ================= TOP CATEGORY =================
    category_sum = expense_df.groupby('category')['amount'].sum()
    total_expense = category_sum.sum()

    if not category_sum.empty:
        top_category = category_sum.idxmax()
        top_amount = category_sum.max()
        top_percentage = (top_amount / total_expense) * 100
    else:
        top_category, top_amount, top_percentage = "N/A", 0, 0

    insights['top_category'] = {
        "name": top_category,
        "amount": round(top_amount, 2),
        "percentage": round(top_percentage, 1)
    }

    # ================= SAVINGS RATE =================
    income = df[df['type'] == 'Income']['amount'].sum()
    expense = expense_df['amount'].sum()

    savings_rate = ((income - expense) / income) * 100 if income > 0 else 0
    insights['savings_rate'] = round(savings_rate, 1)

    # ================= CATEGORY BREAKDOWN =================
    breakdown = []
    for cat, amt in category_sum.items():
        breakdown.append({
            "category": cat,
            "amount": round(amt, 2),
            "percentage": round((amt / total_expense) * 100, 1)
        })

    insights['category_breakdown'] = sorted(
        breakdown, key=lambda x: x['amount'], reverse=True
    )

    return insights
