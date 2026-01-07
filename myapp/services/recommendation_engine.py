from myapp.ml.predictor import predict_goal

def generate_smart_recommendations(user, goals, financials):
    recommendations = []

    for goal in goals:
        freq = goal.contributions.count() or 1

        ai = predict_goal(
            goal,
            avg_income=financials["income"],
            avg_expense=financials["expense"],
            contribution_freq=freq
        )

        recommendations.append({
            "goal_id": goal.id,
            "title": goal.title,
            "daily": ai["daily"],
            "monthly": ai["monthly"],
            "achievable": ai["achievable"],
            "confidence": ai["probability"],
        })

    return recommendations
