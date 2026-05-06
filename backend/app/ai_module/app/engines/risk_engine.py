import os
import pickle
import numpy as np
import pandas as pd
from app.ai_module.app.schemas import UserProfile, AllocationBreakdown


# Paths to trained model and preprocessors
MODEL_PATH   = os.path.join(os.path.dirname(__file__), "../ml_model/risk_model.pkl")
SCALER_PATH  = os.path.join(os.path.dirname(__file__), "../ml_model/scaler.pkl")
ENCODER_PATH = os.path.join(os.path.dirname(__file__), "../ml_model/label_encoder.pkl")


# Rule-based Risk Engine

def rule_based_risk(profile: UserProfile, allocation: AllocationBreakdown) -> float:
    """
    Simple rule-based risk scoring.
    Returns a score from 0 (very safe) to 100 (very risky).

    Rules:
    - High crypto allocation → adds risk
    - High stock allocation → adds moderate risk
    - High bond/cash allocation → reduces risk
    - Short time horizon → increases risk (less time to recover from losses)
    - Young age → can tolerate more risk (has time to recover)
    """
    score = 50.0  # start neutral

    # Allocation rules
    score += allocation.crypto * 1.5      # crypto is very volatile
    score += allocation.stocks * 0.3      # stocks add moderate risk
    score -= allocation.bonds * 0.4       # bonds are safe, reduce risk
    score -= allocation.cash * 0.2        # cash is very safe

    # Time horizon: short = riskier (less time to recover)
    if profile.time_horizon < 3:
        score += 15
    elif profile.time_horizon > 10:
        score -= 10

    # Age: older investors should take less risk
    if profile.age > 55:
        score -= 10
    elif profile.age < 30:
        score += 5

    # User's own stated risk tolerance
    tolerance_map = {"low": -15, "medium": 0, "high": +15}
    score += tolerance_map.get(profile.risk_tolerance.lower(), 0)

    return max(0.0, min(100.0, score))


# ML Model Risk Prediction 

def _load_artifacts():
    """
    Loads model, scaler, and label_encoder from disk.
    Returns (model, scaler, label_encoder) or (None, None, None) if any are missing.
    """
    for path in [MODEL_PATH, SCALER_PATH, ENCODER_PATH]:
        if not os.path.exists(path):
            print(f"[WARN] Missing artifact: {path}")
            print("[WARN] Run: python -m app.ml_model.train_model")
            return None, None, None

    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
    with open(SCALER_PATH, "rb") as f:
        scaler = pickle.load(f)
    with open(ENCODER_PATH, "rb") as f:
        label_encoder = pickle.load(f)

    return model, scaler, label_encoder


def ml_predict_risk(profile: UserProfile, allocation: AllocationBreakdown) -> float:
    """
    Uses our trained Decision Tree model to predict risk score.

    Applies the SAME preprocessing as train_model.py:
      - Builds a DataFrame with the same columns (goal, income_usd, savings_usd dropped during training)
      - Encodes categorical columns using the FITTED label_encoder
      - Scales numeric columns using the FITTED scaler

    Falls back to rule-based score if any artifact is missing.
    """
    model, scaler, label_encoder = _load_artifacts()

    if model is None:
        print("[INFO] Falling back to rule-based scoring.")
        return rule_based_risk(profile, allocation)

    # Build DataFrame — column names and order must match training output
    # (after dropping: goal, income_usd, savings_usd, risk_label, expected_return_pct, risk_score)
    new_data = pd.DataFrame([{
        'age':            profile.age,
        'time_horizon':   profile.time_horizon,
        'risk_tolerance': profile.risk_tolerance.lower(),
        'stocks':         allocation.stocks,
        'etfs':           allocation.etfs,
        'bonds':          allocation.bonds,
        'crypto':         allocation.crypto,
        'cash':           allocation.cash,
    }])

    # Mirror training preprocessing exactly
    num_cols = new_data.select_dtypes(exclude=['object']).columns
    obj_cols = new_data.select_dtypes(include=['object']).columns

    # Use transform() NOT fit_transform() — we must use the encodings learned at training time
    for col in obj_cols:
        new_data[col] = label_encoder.transform(new_data[col])

    new_data[num_cols] = scaler.transform(new_data[num_cols])

    predicted_score = model.predict(new_data)[0]
    return float(np.clip(predicted_score, 0, 100))


# Blended Score 

def get_risk_score(profile: UserProfile, allocation: AllocationBreakdown) -> tuple[float, str]:
    """
    Main function called by the graph.
    Blends rule-based + ML scores (50/50 average).

    Returns:
      (risk_score, risk_label)
      e.g. (72.5, "High")
    """
    rule_score = rule_based_risk(profile, allocation)
    ml_score   = ml_predict_risk(profile, allocation)

    # Blend: equal weight average of both approaches
    final_score = round((rule_score + ml_score) / 2, 1)

    if final_score < 33:
        label = "Low"
    elif final_score < 66:
        label = "Medium"
    else:
        label = "High"

    return final_score, label