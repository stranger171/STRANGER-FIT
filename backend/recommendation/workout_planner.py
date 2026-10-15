def build_workout_plan(
    previous_sets: list[dict],
    recommendation: str
) -> list[dict]:

    if not previous_sets:
        return []

    workout_plan = []

    for workout_set in previous_sets:

        planned_set = {
            "set_number": workout_set["set_number"],
            "target_reps": workout_set["reps"],
            "target_weight_kg": workout_set["weight_kg"]
        }

        if recommendation == "increase_reps":
            planned_set["target_reps"] += 1

        elif recommendation == "reduce_load":
            planned_set["target_weight_kg"] = round(
                workout_set["weight_kg"] * 0.95,
                1
            )

        workout_plan.append(planned_set)

    return workout_plan