from __future__ import annotations

from pathlib import Path
from typing import Dict, Any
import warnings

import joblib
import pandas as pd
from sklearn.exceptions import InconsistentVersionWarning

try:
    from src.rule_engine import build_rule_recommendations, detect_deficiencies
    from src.train_model import save_model, train_model
except ModuleNotFoundError:
    from rule_engine import build_rule_recommendations, detect_deficiencies
    from train_model import save_model, train_model


BASE_DIR = Path(__file__).resolve().parents[1]
MODEL_FILE = BASE_DIR / "model" / "diet_recommender.joblib"


def load_model():
    if MODEL_FILE.exists():
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("error", InconsistentVersionWarning)
                return joblib.load(MODEL_FILE)
        except (OSError, ValueError, EOFError, InconsistentVersionWarning) as exc:
            print(f"Rebuilding model because saved model could not be used: {exc}")

    model, _ = train_model()
    save_model(model)
    return model


def generate_personalized_plan(user_input: Dict[str, Any]) -> Dict[str, object]:
    model = load_model()
    user_df = pd.DataFrame([user_input])
    ml_plan = model.predict(user_df)[0]
    deficiencies, reasons = detect_deficiencies(user_input)
    advice = build_rule_recommendations(deficiencies)
    return {
        "ml_recommended_plan": ml_plan,
        "deficiency_risks": deficiencies,
        "rule_reasons": reasons,
        "rule_based_advice": advice,
    }
