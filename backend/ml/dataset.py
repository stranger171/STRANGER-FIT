def build_training_row(
    features: dict,
    encoded_effort: list[int],
    target: str
) -> dict:

    numerical_features = [
        features["total_volume_kg"],
        features["total_reps"],
        features["heaviest_weight_kg"],
        features["average_rpe"]
    ]

    model_features = numerical_features + encoded_effort

    return {
        "features": model_features,
        "target": target
    }