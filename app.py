from __future__ import annotations

from flask import Flask, render_template, request

from src.recommend import generate_personalized_plan

app = Flask(__name__)


def _to_float(value: str, default: float) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    error = None
    form_data = {
        "age": 25,
        "gender": "female",
        "bmi": 23.0,
        "activity_level": "moderate",
        "hemoglobin": 12.5,
        "vitamin_d": 22.0,
        "vitamin_b12": 250.0,
        "protein_intake": 50.0,
        "water_intake": 2.0,
    }

    if request.method == "POST":
        try:
            # ✅ Get user input
            user_input = {
                "age": _to_float(request.form.get("age"), 25),
                "gender": request.form.get("gender", "female"),
                "bmi": _to_float(request.form.get("bmi"), 23.0),
                "activity_level": request.form.get("activity_level", "moderate"),
                "hemoglobin": _to_float(request.form.get("hemoglobin"), 12.5),
                "vitamin_d": _to_float(request.form.get("vitamin_d"), 22.0),
                "vitamin_b12": _to_float(request.form.get("vitamin_b12"), 250.0),
                "protein_intake": _to_float(request.form.get("protein_intake"), 50.0),
                "water_intake": _to_float(request.form.get("water_intake"), 2.0),
            }

            form_data = user_input
            print("USER INPUT:", user_input)  # 🔍 Debug

            # ✅ Generate plan
            output = generate_personalized_plan(user_input)

            print("MODEL OUTPUT:", output)  # 🔍 Debug

            # ✅ Ensure proper structure for frontend
            result = {
                "ml_recommended_plan": output.get("ml_recommended_plan", "No plan generated"),
                "deficiency_risks": output.get("deficiency_risks", []),
                "rule_reasons": output.get("rule_reasons", {}),
                "rule_based_advice": output.get("rule_based_advice", [])
            }

        except Exception as exc:
            error = f"Error: {str(exc)}"
            print("ERROR:", exc)

    return render_template("index.html", result=result, error=error, form_data=form_data)


if __name__ == "__main__":
    app.run(debug=True)