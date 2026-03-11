from __future__ import annotations

from pathlib import Path
import joblib

from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier


MODEL_PATH = Path("app/ml/model.pkl")


def train_and_save_model() -> None:
    iris = load_iris()
    X = iris.data
    y = iris.target

    model = RandomForestClassifier(random_state=42)
    model.fit(X, y)

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)

    print(f"Model saved to {MODEL_PATH}")


if __name__ == "__main__":
    train_and_save_model()