from __future__ import annotations

from pathlib import Path
from typing import Tuple

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
MODEL_DIR = BASE_DIR / "model"
DATA_FILE = DATA_DIR / "nutrition_data.csv"
MODEL_FILE = MODEL_DIR / "diet_recommender.joblib"


def _generate_synthetic_dataset(n: int = 450) -> pd.DataFrame:
    rng = np.random.default_rng(42)
    ages = rng.integers(18, 61, size=n)
    gender = rng.choice(["male", "female"], size=n)
    bmi = np.round(rng.normal(24.5, 4.2, size=n), 1)
    activity = rng.choice(["low", "moderate", "high"], p=[0.35, 0.45, 0.2], size=n)
    hemoglobin = np.round(rng.normal(13.0, 1.6, size=n), 1)
    vitamin_d = np.round(rng.normal(24.0, 8.0, size=n), 1)
    vitamin_b12 = np.round(rng.normal(280.0, 90.0, size=n), 0)
    protein_intake = np.round(rng.normal(52.0, 13.0, size=n), 1)
    water_intake = np.round(rng.normal(2.0, 0.6, size=n), 1)

    labels = []
    for i in range(n):
        low_nutrients = sum(
            [
                hemoglobin[i] < 12.0,
                vitamin_d[i] < 20.0,
                vitamin_b12[i] < 200.0,
                protein_intake[i] < 45.0,
                water_intake[i] < 1.5,
            ]
        )
        if low_nutrients >= 3:
            labels.append("Recovery Diet Plan")
        elif bmi[i] >= 28.0:
            labels.append("Weight Management Plan")
        elif activity[i] == "high" and protein_intake[i] >= 55.0:
            labels.append("High Protein Performance Plan")
        else:
            labels.append("Balanced Indian Diet Plan")

    return pd.DataFrame(
        {
            "age": ages,
            "gender": gender,
            "bmi": bmi,
            "activity_level": activity,
            "hemoglobin": hemoglobin,
            "vitamin_d": vitamin_d,
            "vitamin_b12": vitamin_b12,
            "protein_intake": protein_intake,
            "water_intake": water_intake,
            "diet_plan": labels,
        }
    )


def prepare_data() -> pd.DataFrame:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if DATA_FILE.exists():
        return pd.read_csv(DATA_FILE)
    data = _generate_synthetic_dataset()
    data.to_csv(DATA_FILE, index=False)
    return data


def train_model() -> Tuple[Pipeline, pd.DataFrame]:
    df = prepare_data()
    x = df.drop(columns=["diet_plan"])
    y = df["diet_plan"]
    x_train, x_test, y_train, _ = train_test_split(
        x, y, test_size=0.2, random_state=42, stratify=y
    )

    num_cols = [
        "age",
        "bmi",
        "hemoglobin",
        "vitamin_d",
        "vitamin_b12",
        "protein_intake",
        "water_intake",
    ]
    cat_cols = ["gender", "activity_level"]

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), num_cols),
            ("cat", OneHotEncoder(handle_unknown="ignore"), cat_cols),
        ]
    )
    model = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("classifier", RandomForestClassifier(n_estimators=200, random_state=42)),
        ]
    )
    model.fit(x_train, y_train)
    print(f"Auto training complete on {len(x_train)} samples.")
    return model, df


def save_model(model: Pipeline) -> None:
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_FILE)
    print(f"Model saved to: {MODEL_FILE}")


if __name__ == "__main__":
    trained_model, _ = train_model()
    save_model(trained_model)
