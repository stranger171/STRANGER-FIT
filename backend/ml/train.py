from pathlib import Path

import joblib
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split


# Project paths
BASE_DIR = Path(__file__).resolve().parent

DATA_PATH = BASE_DIR / "synthetic_workout_dataset.csv"
MODEL_PATH = BASE_DIR / "progression_model.pkl"


# Load dataset
df = pd.read_csv(DATA_PATH)


# Features
X = df[
    [
        "volume_change_percent",
        "reps_change",
        "weight_change_kg",
        "rpe_change"
    ]
]


# Target
y = df["progression"]


# Train/Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


# Create ML model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)


# Train model
model.fit(X_train, y_train)


# Predict test data
y_pred = model.predict(X_test)


# Evaluate model
accuracy = accuracy_score(y_test, y_pred)

print("Model training completed.")
print("Accuracy:", accuracy)

print("\nClassification Report:")
print(
    classification_report(
        y_test,
        y_pred,
        labels=["Improving", "Stable", "Declining"]
    )
)


# Save trained model
joblib.dump(model, MODEL_PATH)

print("\nModel saved successfully:")
print(MODEL_PATH)