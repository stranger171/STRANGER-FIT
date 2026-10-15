import random
import csv


def generate_workout_pair(
    base_weight: float,
    base_reps: int,
    number_of_sets: int = 4,
    base_rpe: float = 7.5,
    scenario: str | None = None
) -> dict:

    previous_sets = []

    for set_number in range(1, number_of_sets + 1):

        weight = base_weight + ((set_number - 1) * 5)

        reps = max(
            5,
            base_reps - ((set_number - 1) * 2)
        )

        rpe = base_rpe + ((set_number - 1) * 0.3)

        rpe += random.choice([
            -0.1,
            0,
            0.1
        ])

        rpe = round(
            min(rpe, 10.0),
            1
        )

        previous_sets.append({
            "set_number": set_number,
            "reps": reps,
            "weight_kg": weight,
            "rpe": rpe
        })

    # Decide workout scenario
    if scenario == "improving":

        weight_change = 2.5

    elif scenario == "declining":

        weight_change = -2.5

    elif scenario == "stable":

        weight_change = 0

    else:

        weight_change = random.choice([
            -2.5,
            0,
            2.5
        ])

    current_sets = []

    for previous_set in previous_sets:

        current_weight = (
            previous_set["weight_kg"]
            + weight_change
        )

        previous_reps = previous_set["reps"]

        if scenario == "improving":

            current_reps = previous_reps

            rpe_change = random.choice([
                -0.1,
                0,
                0.1
            ])

        elif scenario == "declining":

            current_reps = (
                previous_reps
                - random.choice([0, 1])
            )

            rpe_change = random.choice([
                0.5,
                0.6,
                0.7
            ])

        elif scenario == "stable":

            current_reps = previous_reps

            rpe_change = 0

        else:

            if weight_change > 0:

                current_reps = (
                    previous_reps
                    - random.choice([0, 1])
                )

                rpe_change = random.choice([
                    0.2,
                    0.3,
                    0.4
                ])

            elif weight_change < 0:

                current_reps = (
                    previous_reps
                    + random.choice([0, 1])
                )

                rpe_change = random.choice([
                    -0.1,
                    -0.2,
                    -0.3
                ])

            else:

                current_reps = (
                    previous_reps
                    + random.choice([-1, 0, 1])
                )

                rpe_change = random.choice([
                    -0.1,
                    0,
                    0.1
                ])

        current_reps = max(
            5,
            current_reps
        )

        current_rpe = (
            previous_set["rpe"]
            + rpe_change
        )

        current_rpe = round(
            min(max(current_rpe, 5.0), 10.0),
            1
        )

        current_sets.append({
            "set_number": previous_set["set_number"],
            "reps": current_reps,
            "weight_kg": current_weight,
            "rpe": current_rpe
        })

    return {
        "previous_sets": previous_sets,
        "current_sets": current_sets
    }


def calculate_workout_changes(
    previous_sets: list[dict],
    current_sets: list[dict]
) -> dict:

    previous_volume = sum(
        workout_set["reps"] * workout_set["weight_kg"]
        for workout_set in previous_sets
    )

    current_volume = sum(
        workout_set["reps"] * workout_set["weight_kg"]
        for workout_set in current_sets
    )

    previous_reps = sum(
        workout_set["reps"]
        for workout_set in previous_sets
    )

    current_reps = sum(
        workout_set["reps"]
        for workout_set in current_sets
    )

    previous_heaviest_weight = max(
        workout_set["weight_kg"]
        for workout_set in previous_sets
    )

    current_heaviest_weight = max(
        workout_set["weight_kg"]
        for workout_set in current_sets
    )

    previous_average_rpe = sum(
        workout_set["rpe"]
        for workout_set in previous_sets
    ) / len(previous_sets)

    current_average_rpe = sum(
        workout_set["rpe"]
        for workout_set in current_sets
    ) / len(current_sets)

    if previous_volume == 0:
        volume_change_percent = 0
    else:
        volume_change_percent = (
            (current_volume - previous_volume)
            / previous_volume
        ) * 100

    return {
        "previous_volume_kg": round(previous_volume, 2),
        "current_volume_kg": round(current_volume, 2),
        "volume_change_percent": round(
            volume_change_percent,
            2
        ),
        "previous_reps": previous_reps,
        "current_reps": current_reps,
        "reps_change": current_reps - previous_reps,
        "previous_heaviest_weight_kg": previous_heaviest_weight,
        "current_heaviest_weight_kg": current_heaviest_weight,
        "weight_change_kg": round(
            current_heaviest_weight
            - previous_heaviest_weight,
            2
        ),
        "previous_average_rpe": round(
            previous_average_rpe,
            2
        ),
        "current_average_rpe": round(
            current_average_rpe,
            2
        ),
        "rpe_change": round(
            current_average_rpe
            - previous_average_rpe,
            2
        )
    }




def classify_progression(changes: dict) -> str:

    score = 0

    # Volume signal
    if changes["volume_change_percent"] >= 3:
        score += 1

    elif changes["volume_change_percent"] <= -3:
        score -= 1

    # Heaviest weight signal
    if changes["weight_change_kg"] > 0:
        score += 2

    elif changes["weight_change_kg"] < 0:
        score -= 2

    # Reps signal
    if changes["reps_change"] > 0:
        score += 1

    elif changes["reps_change"] < 0:
        score -= 1

    # RPE signal
    if changes["rpe_change"] <= -0.2:
        score += 1

    elif changes["rpe_change"] >= 0.5:
        score -= 1

    # Final classification
    if score >= 2:
        return "Improving"

    elif score <= -2:
        return "Declining"

    return "Stable"





def generate_training_data(
    number_of_samples: int = 12
) -> list[dict]:

    dataset = []

    scenarios = [
        "improving",
        "stable",
        "declining"
    ]

    for index in range(number_of_samples):

        scenario = scenarios[index % 3]

        pair = generate_workout_pair(
            base_weight=random.choice([
                40,
                45,
                50,
                55,
                60
            ]),
            base_reps=random.choice([
                8,
                10,
                12
            ]),
            number_of_sets=4,
            base_rpe=random.choice([
                7.0,
                7.5,
                8.0
            ]),
            scenario=scenario
        )

        changes = calculate_workout_changes(
            pair["previous_sets"],
            pair["current_sets"]
        )

        progression = classify_progression(changes)

        dataset.append({
            "volume_change_percent": changes[
                "volume_change_percent"
            ],
            "reps_change": changes[
                "reps_change"
            ],
            "weight_change_kg": changes[
                "weight_change_kg"
            ],
            "rpe_change": changes[
                "rpe_change"
            ],
            "progression": progression
        })

    return dataset


def save_dataset_to_csv(
    dataset: list[dict],
    filename: str = "synthetic_workout_dataset.csv"
) -> None:

    fieldnames = [
        "volume_change_percent",
        "reps_change",
        "weight_change_kg",
        "rpe_change",
        "progression"
    ]

    with open(filename, "w", newline="") as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()

        writer.writerows(dataset)