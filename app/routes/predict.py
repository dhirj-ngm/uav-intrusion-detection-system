import os
import pandas as pd
from flask import Blueprint, request, jsonify, current_app

from app import db
from app.models.prediction import Prediction
from app.services import ml_service

predict_bp = Blueprint("predict", __name__)


def _threat_level(label, confidence):
    if label == "Normal Traffic":
        return "Low"
    return "High" if confidence >= 0.85 else "Medium"


@predict_bp.route("/predict", methods=["POST"])
def predict_attacks():
    data = request.get_json(silent=True) or {}
    batch_id = data.get("filename")

    if not batch_id:
        return jsonify({"success": False, "message": "filename is required"}), 400

    csv_path = os.path.join(current_app.config["UPLOAD_FOLDER"], f"{batch_id}.csv")
    if not os.path.exists(csv_path):
        return jsonify({"success": False, "message": "No uploaded file found"}), 404

    df = pd.read_csv(csv_path)

    artifact = ml_service.load_model()
    feature_columns = artifact["feature_columns"]

    missing_cols = [c for c in feature_columns if c not in df.columns]
    if missing_cols:
        return jsonify({"success": False, "message": f"Missing expected columns: {missing_cols}"}), 400

    has_ground_truth = "label" in df.columns
    has_flow_id = "FlowID" in df.columns
    feature_rows = df[feature_columns].to_dict(orient="records")

    raw_results = ml_service.predict_batch(feature_rows)

    formatted_results = []
    for i, result in enumerate(raw_results):
        label = result["predicted_label"]
        confidence = result["confidence"]

        pred = Prediction(
            features=feature_rows[i],
            predicted_class_id=result["predicted_class_id"],
            predicted_label=label,
            confidence=confidence,
            true_label=str(df.iloc[i]["label"]) if has_ground_truth else None,
            batch_id=batch_id,
            prediction_time_ms=result["prediction_time_ms"],
        )
        db.session.add(pred)

        formatted_results.append({
            "flowId": str(df.iloc[i]["FlowID"]) if has_flow_id else str(i + 1),
            "predictedAttack": label,
            "confidence": round(confidence * 100, 1),
            "threatLevel": _threat_level(label, confidence),
        })

    db.session.commit()

    attack_count = sum(1 for r in formatted_results if r["predictedAttack"] != "Normal Traffic")
    normal_count = len(formatted_results) - attack_count

    return jsonify({
        "success": True,
        "summary": f"Processed {len(formatted_results)} rows — {attack_count} attacks detected, {normal_count} normal.",
        "results": formatted_results,
    }), 200