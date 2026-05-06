"""
ML Model Training Script

Trains a simple Decision Tree to predict portfolio risk score (0-100).

Features (X):
  age, time_horizon, risk_tolerance_encoded, stocks%, etfs%, bonds%, crypto%, cash%

Target (y):
  risk_score (0-100)

We generate synthetic training data using our rule-based engine,
then train the model and save it as risk_model.pkl

"""

import pickle
import os
import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from sklearn.preprocessing import LabelEncoder, StandardScaler


def training_data(dataset: pd.DataFrame, label_encoder: LabelEncoder, scaler: StandardScaler):
    """
    Preprocesses the dataset for training.

    Drops unused columns, encodes categoricals, scales numerics.
    Returns (X, y) where X is the feature DataFrame and y is the target array.
    """
    data = dataset.drop([
        'risk_label',
        'expected_return_pct',
        'risk_score',
        'income_usd',
        'savings_usd',
        'goal',               # dropped per preprocessing function
    ], axis=1)

    num_cols = data.select_dtypes(exclude=['object']).columns
    obj_cols = data.select_dtypes(include=['object']).columns

    # Fit AND transform on training data
    for col in obj_cols:
        data[col] = label_encoder.fit_transform(data[col])

    data[num_cols] = scaler.fit_transform(data[num_cols])

    y = dataset['risk_score'].values
    X = data

    return X, y


def train_and_save():
    """
    Full training pipeline:
    1. Load data
    2. Preprocess (fit scaler + encoder on training data)
    3. Split into train/test
    4. Train Decision Tree
    5. Evaluate accuracy
    6. Save model, scaler, and label_encoder to disk
    """
    dataset = pd.read_csv("risk_training_data.csv")

    # Instantiate preprocessors fresh each run so they're fitted on THIS data
    label_encoder = LabelEncoder()
    scaler = StandardScaler()

    X, y = training_data(dataset.copy(), label_encoder, scaler)

    # Split: 80% train, 20% test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    print(f"Training samples: {len(X_train)}, Test samples: {len(X_test)}")

    # Train the model
    print("Training Decision Tree...")
    model = DecisionTreeRegressor(
        max_depth=8,
        min_samples_leaf=10,
        random_state=42,
    )
    model.fit(X_train, y_train)

    # Evaluate on test set
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    print(f"Mean Absolute Error: {mae:.2f} points (out of 100)")
    print(f"That means predictions are off by ~{mae:.0f} points on average")

    # Save model, scaler, and label_encoder — all three needed for predict.py
    model_dir = os.path.dirname(__file__)

    model_path = os.path.join(model_dir, "risk_model.pkl")
    scaler_path = os.path.join(model_dir, "scaler.pkl")
    encoder_path = os.path.join(model_dir, "label_encoder.pkl")

    with open(model_path, "wb") as f:
        pickle.dump(model, f)

    with open(scaler_path, "wb") as f:         # <-- NEW
        pickle.dump(scaler, f)

    with open(encoder_path, "wb") as f:        # <-- NEW
        pickle.dump(label_encoder, f)

    print(f"Model saved to:         {model_path}")
    print(f"Scaler saved to:        {scaler_path}")
    print(f"Label encoder saved to: {encoder_path}")
    print("Training complete!")

    return model, mae


if __name__ == "__main__":
    train_and_save()

