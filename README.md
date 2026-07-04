# Nutrition Deficiency & Personalized Diet Recommendation (No Dataset Needed)

This is a full AI/ML project with a Flask web UI.

## Features

- No manual dataset required
- Synthetic dataset is generated automatically
- Model is auto-trained and saved if missing
- Rule-based nutrition deficiency detection
- Personalized diet plan recommendation

## Project Structure

- `app.py` - Flask app with web form
- `src/train_model.py` - synthetic data generation + ML model training
- `src/recommend.py` - auto model load/train and prediction
- `src/rule_engine.py` - deficiency detection and advice
- `templates/index.html` - web UI template

## Setup

```bash
pip install -r requirements.txt
```

## Run

```bash
python app.py
```

Then open: `http://127.0.0.1:5000`
