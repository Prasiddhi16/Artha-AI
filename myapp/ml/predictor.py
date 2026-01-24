# myapp/ml/predictor.py

import joblib
import os
import numpy as np
from datetime import date
from decimal import Decimal

MODEL_PATH = os.path.join(os.path.dirname(__file__), "goal_predictor.pkl")

try:
    model = joblib.load(MODEL_PATH)
except FileNotFoundError:
    model = None
    print(f"Warning: ML model not found at {MODEL_PATH}. Using rule-based fallback.")


def predict_goal(goal, avg_income, avg_expense, contribution_freq=1):
    """
    Predict goal achievement and suggest contributions.
    """

    target = Decimal(goal.target_amount)
    current = Decimal(getattr(goal, "total_contributed", 0))
    avg_income = Decimal(avg_income)
    avg_expense = Decimal(avg_expense)

    remaining = max(target - current, Decimal("0"))
    days_left = max((goal.target_date - date.today()).days, 1)

   
    if model is None:
        daily = remaining / Decimal(days_left)
        monthly = daily * Decimal(30)

        achievable = daily <= (avg_income / Decimal(2))
        probability = min(
            Decimal("1.0"),
            (current / target) if target > 0 else Decimal("0")
        )

        return {
            "daily": float(round(daily, 2)),
            "monthly": float(round(monthly, 2)),
            "achievable": bool(achievable),
            "probability": float(round(probability, 2)),
        }

   
    features = np.array([
        float(target),
        float(current),
        float(remaining),
        float(avg_income),
        float(avg_expense),
        contribution_freq,
        days_left
    ]).reshape(1, -1)

    try:
        probability = model.predict_proba(features)[0][1]
    except AttributeError:
        probability = float(
            min(max(model.predict(features)[0], 0), 1)
        )

    daily = remaining / Decimal(days_left)
    monthly = daily * Decimal(30)
    achievable = probability >= 0.5

    return {
        "daily": float(round(daily, 2)),
        "monthly": float(round(monthly, 2)),
        "achievable": bool(achievable),
        "probability": round(probability, 2),
    }
