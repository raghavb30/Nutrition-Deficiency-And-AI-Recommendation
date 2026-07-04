from __future__ import annotations

from typing import Dict, List, Tuple


DeficiencyResult = Tuple[List[str], Dict[str, str]]


def _flag(value: float, threshold: float) -> bool:
    return value < threshold


def detect_deficiencies(user_input: Dict[str, float]) -> DeficiencyResult:
    deficiencies: List[str] = []
    reasons: Dict[str, str] = {}

    if _flag(user_input.get("hemoglobin", 13.0), 12.0):
        deficiencies.append("Iron")
        reasons["Iron"] = "Low hemoglobin indicates possible iron deficiency."

    if _flag(user_input.get("vitamin_d", 30.0), 20.0):
        deficiencies.append("Vitamin D")
        reasons["Vitamin D"] = "Low vitamin D level may affect bones and immunity."

    if _flag(user_input.get("vitamin_b12", 300.0), 200.0):
        deficiencies.append("Vitamin B12")
        reasons["Vitamin B12"] = "Low B12 level can cause fatigue and nerve symptoms."

    if _flag(user_input.get("protein_intake", 60.0), 45.0):
        deficiencies.append("Protein")
        reasons["Protein"] = "Daily protein intake appears low for healthy recovery."

    if _flag(user_input.get("water_intake", 2.0), 1.5):
        deficiencies.append("Hydration")
        reasons["Hydration"] = "Water intake is low and may reduce performance."

    return deficiencies, reasons


def build_rule_recommendations(deficiencies: List[str]) -> List[str]:
    recommendations = {
        "Iron": "Include spinach, lentils, beetroot, jaggery, and vitamin-C rich fruits.",
        "Vitamin D": "Add sunlight exposure and foods like fortified milk, egg yolk, and mushrooms.",
        "Vitamin B12": "Eat dairy, eggs, fish/chicken, or fortified cereals.",
        "Protein": "Increase paneer, dal, soy, eggs, chicken, and curd portions.",
        "Hydration": "Target 2.5-3 liters water, include coconut water and soups.",
    }
    advice = [recommendations[item] for item in deficiencies if item in recommendations]
    if not advice:
        advice.append("Maintain a balanced diet with a variety of fruits, vegetables, whole grains, lean proteins, and healthy fats. Stay hydrated and active.")
    return advice
