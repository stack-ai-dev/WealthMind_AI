"""
Simple prediction helper.

This is a thin wrapper around the model loading + prediction logic.
The risk_engine.py calls get_risk_score() from here.

Usage:
  python -m app.ai_module.app.ml_model.predict
"""

import os
import pickle
import numpy as np
from typing import Optional

import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler


MODEL_PATH = os.path.join(os.path.dirname(__file__), "risk_model.pkl")
SCALER_PATH = os.path.join(os.path.dirname(__file__), "scaler.pkl")
ENCODER_PATH = os.path.join(os.path.dirname(__file__), "label_encoder.pkl")


def load_model():
    """
    Loads the trained model from disk.
    Returns None if model file doesn't exist.
    """
    if not os.path.exists(MODEL_PATH):
        print(f"[WARN] Model file not found at: {MODEL_PATH}")
        print("[WARN] Run: python -m app.ml_model.train_model")
        return None

    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
    return model


def load_preprocessors():
    """
    Loads the fitted scaler and label encoder saved during training.
    Returns (None, None) if files don't exist.
    """
    if not os.path.exists(SCALER_PATH) or not os.path.exists(ENCODER_PATH):
        print("[WARN] Preprocessor files not found. Re-run train_model.py.")
        return None, None

    with open(SCALER_PATH, "rb") as f:
        scaler = pickle.load(f)

    with open(ENCODER_PATH, "rb") as f:
        label_encoder = pickle.load(f)

    return scaler, label_encoder


def predict_risk_score(
    stocks: float,
    etfs: float,
    bonds: float,
    crypto: float,
    cash: float,
    age: int,
    time_horizon: int,
    risk_tolerance: str,   # "low", "medium", "high"
) -> Optional[float]:
    """
    Predicts risk score for a given portfolio configuration.

    Returns:
        float: risk score between 0 and 100
        None: if model or preprocessors aren't available
    """
    model = load_model()
    if model is None:
        return None

    scaler, label_encoder = load_preprocessors()
    if scaler is None or label_encoder is None:
        return None

    # Build a DataFrame matching the training feature columns
    # (after dropping: risk_label, expected_return_pct, risk_score, income_usd, savings_usd, goal)
    new_data = pd.DataFrame([{
        'age': age,
        'time_horizon': time_horizon,
        'risk_tolerance': risk_tolerance,
        'stocks': stocks,
        'etfs': etfs,
        'bonds': bonds,
        'crypto': crypto,
        'cash': cash,
    }])

    # Separate numeric and object columns — mirrors training preprocessing
    num_cols = new_data.select_dtypes(exclude=['object']).columns
    obj_cols = new_data.select_dtypes(include=['object']).columns

    # Encode categorical columns using the FITTED label encoder from training
    for col in obj_cols:
        new_data[col] = label_encoder.transform(new_data[col])

    # Scale numeric columns using the FITTED scaler from training
    new_data[num_cols] = scaler.transform(new_data[num_cols])

    score = model.predict(new_data)[0]
    return float(np.clip(score, 0, 100))


def get_feature_importance() -> dict:
    """
    Returns which features matter most for risk prediction.
    Great for explainability / debugging.
    """
    model = load_model()
    if model is None:
        return {}

    feature_names = [
        "Age", "Time Horizon", "Risk Tolerance",
        "Stocks %", "ETFs %", "Bonds %", "Crypto %", "Cash %",
    ]

    importances = model.feature_importances_
    return {
        name: round(float(imp) * 100, 1)
        for name, imp in zip(feature_names, importances)
    }


# if __name__ == "__main__":
#     stocks = float(input("Enter percentage allocation to stocks: "))
#     etfs = float(input("Enter percentage allocation to ETFs: "))
#     bonds = float(input("Enter percentage allocation to bonds: "))
#     crypto = float(input("Enter percentage allocation to crypto: "))
#     cash = float(input("Enter percentage allocation to cash: "))
#     age = int(input("Enter your age: "))
#     time_horizon = int(input("Enter your investment time horizon (in years): "))
#     risk_tolerance = input("Enter your risk tolerance (low, medium, high): ")


#     score = predict_risk_score(stocks, etfs, bonds, crypto, cash, age, time_horizon, risk_tolerance)
#     print("\nPredicted risk score:", score)
