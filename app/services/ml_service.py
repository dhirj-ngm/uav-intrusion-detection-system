import time
import joblib
import numpy as np
import pandas as pd
from flask import current_app

_artifact = None


def load_model():
    global _artifact
    if _artifact is None:
        model_path = current_app.config["MODEL_PATH"]
        _artifact = joblib.load(model_path)
    return _artifact


def predict_batch(feature_rows: list[dict]) -> list[dict]:
    artifact = load_model()
    model = artifact["model"]
    feature_columns = artifact["feature_columns"]
    feature_dtypes = artifact["feature_dtypes"]
    class_names = artifact["class_names"]

    df = pd.DataFrame(feature_rows)

    missing = set(feature_columns) - set(df.columns)
    if missing:
        raise ValueError(f"Missing Features: {missing}")

    df = df[feature_columns]

    for col, dtype in feature_dtypes.items():
        df[col] = df[col].astype(dtype)

    start = time.perf_counter()
    predictions = model.predict(df)
    probabilities = model.predict_proba(df)
    elapsed_ms = (time.perf_counter() - start) * 1000 / max(len(df), 1)

    results = []
    for pred, proba in zip(predictions, probabilities):
        results.append({
            "predicted_class_id": int(pred),
            "predicted_label": class_names[pred],
            "confidence": float(proba.max()),
            "prediction_time_ms": round(elapsed_ms, 3),
        })
    return results