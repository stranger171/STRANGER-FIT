import re
import json
from pathlib import Path
from difflib import SequenceMatcher

def normalize_exercise_text(exercise_name: str) -> str:
    """
    Clean and normalize raw exercise text.
    """

    # Convert to lowercase
    text = exercise_name.lower()

    # Replace hyphens and underscores with spaces
    text = re.sub(r"[-_]", " ", text)

    # Remove unwanted punctuation
    text = re.sub(r"[^a-z0-9\s]", "", text)

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text)

    # Remove leading/trailing spaces
    text = text.strip()

    return text





BASE_DIR = Path(__file__).resolve().parent.parent
EXERCISE_CATALOG_PATH = BASE_DIR / "data" / "exercises.json"


def load_exercise_catalog() -> list[dict]:
    with open(EXERCISE_CATALOG_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def find_exact_exercise_match(
    exercise_name: str
) -> str | None:

    normalized_input = normalize_exercise_text(
        exercise_name
    )

    catalog = load_exercise_catalog()

    for exercise in catalog:

        canonical_name = exercise["canonical_name"]

        if normalized_input == normalize_exercise_text(
            canonical_name
        ):
            return canonical_name

        for alias in exercise["aliases"]:

            if normalized_input == normalize_exercise_text(
                alias
            ):
                return canonical_name

    return None


def find_fuzzy_exercise_match(
    exercise_name: str,
    threshold: float = 0.85
) -> dict | None:

    normalized_input = normalize_exercise_text(
        exercise_name
    )

    catalog = load_exercise_catalog()

    best_match = None
    best_score = 0.0

    for exercise in catalog:

        canonical_name = exercise["canonical_name"]

        candidates = [
            canonical_name,
            *exercise["aliases"]
        ]

        for candidate in candidates:

            normalized_candidate = normalize_exercise_text(
                candidate
            )

            score = SequenceMatcher(
                None,
                normalized_input,
                normalized_candidate
            ).ratio()

            if score > best_score:
                best_score = score
                best_match = canonical_name

    if best_score >= threshold:

        return {
            "canonical_name": best_match,
            "confidence": round(best_score, 2)
        }

    return None




def normalize_exercise_name(
    exercise_name: str
) -> dict:

    # Step 1: Clean the input
    normalized_input = normalize_exercise_text(
        exercise_name
    )

    if not normalized_input:
        return {
            "status": "invalid",
            "canonical_name": None,
            "method": None
        }

    # Step 2: Try exact / alias matching
    exact_match = find_exact_exercise_match(
        normalized_input
    )

    if exact_match:
        return {
            "status": "matched",
            "canonical_name": exact_match,
            "method": "exact"
        }

    # Step 3: Try fuzzy matching
    fuzzy_match = find_fuzzy_exercise_match(
        normalized_input
    )

    if fuzzy_match:
        return {
            "status": "matched",
            "canonical_name": fuzzy_match["canonical_name"],
            "method": "fuzzy",
            "confidence": fuzzy_match["confidence"]
        }

    # Step 4: Use Gemini only when matching fails
    from services.exercise_llm import normalize_unknown_exercise

    llm_result = normalize_unknown_exercise(
        normalized_input
    )

    if llm_result is None:
        return {
            "status": "unrecognized",
            "canonical_name": None,
            "method": "llm"
        }

    return {
        "status": "normalized",
        "canonical_name": llm_result,
        "method": "llm"
    }