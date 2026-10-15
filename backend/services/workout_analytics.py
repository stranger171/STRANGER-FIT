def detect_load_pattern(weights: list[float]) -> str:
    if len(weights) < 2:
        return "Insufficient data"

    increasing = all(
        weights[i] < weights[i + 1]
        for i in range(len(weights) - 1)
    )

    decreasing = all(
        weights[i] > weights[i + 1]
        for i in range(len(weights) - 1)
    )

    if increasing:
        return "Increasing"

    if decreasing:
        return "Decreasing"

    return "Mixed"


def analyze_workout_sets(sets_data: list[dict] | None) -> dict:
    if not sets_data:
      return {
            "pattern": "Insufficient data",
            "weights": [],
            "total_sets": 0,
            "total_reps": 0,
            "total_volume_kg": 0,
            "heaviest_weight_kg": 0,
            "average_rpe": None,
            "effort_level": "Insufficient data"
 }

    weights = [
        workout_set["weight_kg"]
        for workout_set in sets_data
    ]

    total_reps = sum(
        workout_set["reps"]
        for workout_set in sets_data
    )

    total_volume = sum(
        workout_set["weight_kg"] * workout_set["reps"]
        for workout_set in sets_data
    )

    heaviest_weight = max(weights)

    pattern = detect_load_pattern(weights)
    average_rpe = calculate_average_rpe(sets_data)
    effort_level = classify_effort_level(average_rpe)

    return {
        "pattern": pattern,
        "weights": weights,
        "total_sets": len(sets_data),
        "total_reps": total_reps,
        "total_volume_kg": total_volume,
        "heaviest_weight_kg": heaviest_weight,
        "average_rpe": average_rpe,
        "effort_level": effort_level
    }


def calculate_average_rpe(sets_data: list[dict] | None) -> float | None:

    if not sets_data:
        return None

    rpes = [
        workout_set["rpe"]
        for workout_set in sets_data
        if workout_set.get("rpe") is not None
    ]

    if not rpes:
        return None

    return round(sum(rpes) / len(rpes), 2)


def detect_rpe_trend(
    previous_rpe: float | None,
    current_rpe: float | None
) -> str:

    if previous_rpe is None or current_rpe is None:
        return "Insufficient data"

    if current_rpe > previous_rpe:
        return "Increasing"

    if current_rpe < previous_rpe:
        return "Decreasing"

    return "Stable"


def classify_effort_level(average_rpe: float | None) -> str:

    if average_rpe is None:
        return "Insufficient data"

    if average_rpe < 7:
        return "Low"

    if average_rpe <= 8:
        return "Moderate"

    return "High"


def compare_workouts(
    previous: dict,
    current: dict
) -> dict:

    previous_volume = previous["total_volume_kg"]
    current_volume = current["total_volume_kg"]

    previous_heaviest = previous["heaviest_weight_kg"]
    current_heaviest = current["heaviest_weight_kg"]

    previous_reps = previous["total_reps"]
    current_reps = current["total_reps"]

    volume_change = current_volume - previous_volume
    heaviest_change = current_heaviest - previous_heaviest
    reps_change = current_reps - previous_reps

    if previous_volume > 0:
        volume_change_percent = (
            volume_change / previous_volume
        ) * 100
    else:
        volume_change_percent = 0

    if current_volume > previous_volume and current_heaviest >= previous_heaviest:
        progression = "Improving"

    elif current_volume < previous_volume and current_heaviest < previous_heaviest:
        progression = "Declining"

    elif (
        current_volume == previous_volume
        and current_heaviest == previous_heaviest
    ):
        progression = "Stable"

    else:
        progression = "Mixed"

    return {
        "progression": progression,
        "volume_change_kg": volume_change,
        "volume_change_percent": round(volume_change_percent, 2),
        "heaviest_weight_change_kg": heaviest_change,
        "reps_change": reps_change
    }



def build_performance_summary(
    previous: dict,
    current: dict
) -> dict:

    comparison = compare_workouts(
        previous,
        current
    )
    previous_rpe = previous.get("average_rpe")
    current_rpe = current.get("average_rpe")
    current_effort_level = current.get("effort_level")

    rpe_trend = detect_rpe_trend(
    previous_rpe,
    current_rpe
)

    return {
        "previous": {
            "volume_kg": previous["total_volume_kg"],
            "total_reps": previous["total_reps"],
            "heaviest_weight_kg": previous["heaviest_weight_kg"]
        },
        "current": {
            "volume_kg": current["total_volume_kg"],
            "total_reps": current["total_reps"],
            "heaviest_weight_kg": current["heaviest_weight_kg"]
        },
        "changes": {
            "volume_kg": comparison["volume_change_kg"],
            "volume_percent": comparison["volume_change_percent"],
            "heaviest_weight_kg": comparison["heaviest_weight_change_kg"],
            "reps": comparison["reps_change"]

        },
        "rpe": {
          "previous_average": previous_rpe,
          "current_average": current_rpe,
          "trend": rpe_trend,
          "current_effort_level": current_effort_level

        },
        "progression": comparison["progression"]
    }
