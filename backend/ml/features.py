def build_ml_features(analytics: dict) -> dict:
    return {
        "total_volume_kg": analytics["total_volume_kg"],
        "total_reps": analytics["total_reps"],
        "heaviest_weight_kg": analytics["heaviest_weight_kg"],
        "average_rpe": analytics["average_rpe"],
        "effort_level": analytics["effort_level"],
    }