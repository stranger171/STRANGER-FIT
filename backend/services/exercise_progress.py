from sqlmodel import Session, select

from models.workout import Workout
from services.workout_analytics import (
    analyze_workout_sets,
    build_performance_summary
)
from recommendation.recommendation_service import get_ml_recommendation


def analyze_exercise_progress(
    user_id: int,
    exercise_name: str,
    session: Session
):

    workouts = session.exec(
        select(Workout)
        .where(
            Workout.user_id == user_id,
            Workout.exercise_name == exercise_name
        )
        .order_by(Workout.workout_date)
    ).all()

    history = []

    for workout in workouts:

        analytics = analyze_workout_sets(
            workout.sets_data
        )

        if analytics["total_sets"] > 0:
            history.append({
                "workout_id": workout.id,
                "workout_date": workout.workout_date,
                "exercise_name": workout.exercise_name,
                "sets_data": workout.sets_data,
                "analytics": analytics
            })

    performance_summary = None

    if len(history) >= 2:

        previous = history[-2]["analytics"]
        current = history[-1]["analytics"]

        performance_summary = build_performance_summary(
            previous,
            current
        )

    recommendation = None

    if performance_summary is not None:

        changes = performance_summary["changes"]

        previous_rpe = performance_summary["rpe"]["previous_average"]
        current_rpe = performance_summary["rpe"]["current_average"]

        rpe_change = current_rpe - previous_rpe

        ml_result = get_ml_recommendation(
            volume_change_percent=changes["volume_percent"],
            reps_change=changes["reps"],
            weight_change_kg=changes["heaviest_weight_kg"],
            rpe_change=rpe_change,
            effort_level=performance_summary["rpe"]["current_effort_level"]
        )

        ml_prediction = ml_result["progression"]
        recommendation = ml_result["recommendation"]

    return {
        "history": history,
        "performance_summary": performance_summary,
         "ml_prediction": ml_prediction if performance_summary is not None else None,
        "recommendation": recommendation
    }