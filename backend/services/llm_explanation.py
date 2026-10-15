import os

from dotenv import load_dotenv
from google import genai

load_dotenv()


client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def explain_workout_recommendation(
    progression: str,
    effort_level: str,
    volume_change_percent: float,
    weight_change_kg: float,
    recommendation: str
) -> str:

    prompt = f"""
You are the explanation layer of Stranger Fit.

Explain the existing workout recommendation using only the
information provided below.

Progression: {progression}
Effort level: {effort_level}
Volume change: {volume_change_percent}%
Heaviest weight change: {weight_change_kg} kg
Recommendation: {recommendation}

Rules:
- Do not change the recommendation.
- Do not create a different workout plan.
- Do not give medical or safety claims.
- Do not introduce information that is not provided.
- Explain the reasoning clearly.
- Keep the explanation under 3 sentences.
"""

    chat = client.chats.create(
        model="gemini-3.5-flash-lite"
    )

    response = chat.send_message(prompt)

    return response.text