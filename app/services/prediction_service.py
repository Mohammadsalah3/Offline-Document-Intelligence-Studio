from __future__ import annotations

from pathlib import Path
import sys
import joblib


CLASS_NAMES = ["setosa", "versicolor", "virginica"]


def get_base_path() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys._MEIPASS)
    return Path(__file__).resolve().parents[2]


def get_model_path() -> Path:
    base_path = get_base_path()
    return base_path / "app" / "ml" / "model.pkl"


def load_model():
    model_path = get_model_path()

    if not model_path.exists():
        raise FileNotFoundError(f"Model file not found: {model_path}")

    return joblib.load(model_path)


def predict_iris(features: list[float]) -> dict:
    if len(features) != 4:
        raise ValueError("Exactly 4 features are required.")

    model = load_model()
    prediction = model.predict([features])[0]
    predicted_class = CLASS_NAMES[int(prediction)]

    return {
        "features": features,
        "predicted_class_index": int(prediction),
        "predicted_class_name": predicted_class,
    }