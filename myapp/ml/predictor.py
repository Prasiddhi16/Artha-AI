# myapp/ml/predictor.py

import joblib
import os
import numpy as np
from datetime import date

# Path to your trained ML model (ensure you have goal_predictor.pkl in myapp/ml/)
MODEL_PATH = os.path.join(os.path.dirname(__file__), "goal_predictor.pkl")

try:
    model = joblib.load(MODEL_PATH)
except FileNotFoundError:
    model = None
    print(f"Warning: ML model not found at {MODEL_PATH}. Predictions will fail.")


def predict_goal(goal, avg_income, avg_expense, contribution_freq=1):
    """
    Predict goal achievement and suggest daily/monthly contributions.

    Args:
        goal: Goal object with attributes like target_amount, current_amount, created_date, due_date
        avg_income: User's average monthly income
        avg_expense: User's average monthly expense
        contribution_freq: Number of contributions made / per period

    Returns:
        dict with keys:
            - daily: recommended daily contribution
            - monthly: recommended monthly contribution
            - achievable: True/False
            - probability: confidence score (0-1)
    """
    # Fallback if no model
    if model is None:
     remaining = max(goal.target_amount - goal.total_contributed, 0)
    days_left = max((goal.target_date - date.today()).days, 1)

    daily = remaining / days_left
    monthly = daily * 30

    # Rule-based achievable: if remaining can be saved in time at daily rate <= 50% of avg_income
    achievable = daily <= (avg_income / 2)
    probability = min(1.0, (goal.total_contributed / goal.target_amount) + ((days_left * daily) / goal.target_amount))

    return {
        "daily": round(daily, 2),
        "monthly": round(monthly, 2),
        "achievable": achievable,
        "probability": round(probability, 2),
    }

    # Calculate features
    target = getattr(goal, "target_amount", 0)
    current = getattr(goal, "total_contributed", 0)
    remaining = max(target - current, 0)
    days_left = max((getattr(goal, "target_date", date.today()) - getattr(goal, "created", date.today())).days, 1)

    features = np.array([
        target,
        current,
        remaining,
        avg_income,
        avg_expense,
        contribution_freq,
        days_left
    ]).reshape(1, -1)

    # Predict probability of achieving goal
    try:
        probability = model.predict_proba(features)[0][1]  # assumes binary classification
    except AttributeError:
        # fallback if model is regression
        probability = min(max(model.predict(features)[0], 0), 1)

    monthly = remaining / max(days_left / 30, 1)
    daily = remaining / days_left
    achievable = probability >= 0.5

    return {
        "daily": round(daily, 2),
        "monthly": round(monthly, 2),
        "achievable": achievable,
        "probability": round(float(probability), 2),
    }
