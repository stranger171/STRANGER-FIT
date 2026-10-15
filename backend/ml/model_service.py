from pathlib import Path

import joblib


BASE_DIR = Path(__file__).resolve().parent

MODEL_PATH = BASE_DIR / "progression_model.pkl"


model = joblib.load(MODEL_PATH)


def predict_progression(
    volume_change_percent: float,
    reps_change: int,
    weight_change_kg: float,
    rpe_change: float
) -> str:

    features = [[
        volume_change_percent,
        reps_change,
        weight_change_kg,
        rpe_change
    ]]

    prediction = model.predict(features)

    return prediction[0]