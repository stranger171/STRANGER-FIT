def get_recommendation(
    progression: str,
    effort_level: str
) -> str:

    if progression == "Improving":
        if effort_level == "High":
            return "maintain_load"

        return "increase_load"

    if progression == "Stable":
        if effort_level == "High":
            return "maintain_load"

        return "increase_reps"

    if progression == "Declining":
        if effort_level == "High":
            return "reduce_load"

        return "maintain_load"

    return "maintain_load"