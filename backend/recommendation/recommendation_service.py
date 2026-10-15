from ml.model_service import predict_progression
from recommendation.decision_engine import get_recommendation


def get_ml_recommendation(
    volume_change_percent: float,
    reps_change: int,
    weight_change_kg: float,
    rpe_change: float,
    effort_level: str
) -> dict:

    progression = predict_progression(
        volume_change_percent=volume_change_percent,
        reps_change=reps_change,
        weight_change_kg=weight_change_kg,
        rpe_change=rpe_change
    )

    recommendation = get_recommendation(
        progression=progression,
        effort_level=effort_level
    )

    return {
        "progression": progression,
        "effort_level": effort_level,
        "recommendation": recommendation
    }