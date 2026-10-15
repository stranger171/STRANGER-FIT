import os

from dotenv import load_dotenv
from google import genai

load_dotenv()


def normalize_unknown_exercise(
    exercise_name: str
) -> str | None:
    """
    Normalize an unknown exercise name using Gemini.
    Return None if the exercise cannot be normalized.
    """

    prompt = f"""
You are the exercise-name normalization layer of Stranger Fit.

User entered:
"{exercise_name}"

Your job:
1. Fix spelling mistakes.
2. Fix spacing and formatting.
3. Understand common exercise abbreviations.
4. Return the standard/common name of the SAME exercise.
5. If the input is a legitimate exercise not in our catalog,
   return its cleaned standard name.
6. If the input is nonsense or not a recognizable exercise,
   return exactly: INVALID

Strict rules:
- Do not invent an exercise.
- Do not change one exercise into another.
- Do not add explanations or quotes.
- Return only the exercise name or INVALID.
"""

    try:
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            print("Gemini API key is missing.")
            return None

        client = genai.Client(api_key=api_key)

        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt
        )

        if not response.text:
            print("Gemini returned an empty response.")
            return None

        result = response.text.strip()

        if not result or result.upper() == "INVALID":
            return None

        # Reject unusually long responses instead of saving them
        # as exercise names.
        if len(result) > 100 or "\n" in result:
            print("Gemini returned an unexpected response.")
            return None

        return result

    except Exception as error:
        print(f"Exercise normalization failed: {error}")
        return None
