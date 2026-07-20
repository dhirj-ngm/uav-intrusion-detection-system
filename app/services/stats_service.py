from app import db
from app.models.prediction import Prediction
from sqlalchemy import func


def get_summary_stats():
    total = db.session.query(func.count(Prediction.id)).scalar() or 0

    normal_count = (
        db.session.query(func.count(Prediction.id))
        .filter(Prediction.predicted_label == "Normal Traffic")
        .scalar() or 0
    )
    attack_count = total - normal_count
    normal_pct = round((normal_count / total) * 100, 1) if total else 0.0

    avg_pred_time = (
        db.session.query(func.avg(Prediction.prediction_time_ms)).scalar() or 0
    )

    labeled_total = (
        db.session.query(func.count(Prediction.id))
        .filter(Prediction.true_label.isnot(None))
        .scalar() or 0
    )
    correct = (
        db.session.query(func.count(Prediction.id))
        .filter(Prediction.true_label == Prediction.predicted_label)
        .scalar() or 0
    )
    accuracy = round((correct / labeled_total) * 100, 2) if labeled_total else None

    attack_ratio = (attack_count / total) if total else 0
    if attack_ratio > 0.15:
        threat_level = "High"
    elif attack_ratio > 0.05:
        threat_level = "Medium"
    else:
        threat_level = "Low"

    return {
        "total_packets": total,
        "normal_traffic_pct": normal_pct,
        "total_attacks": attack_count,
        "model_accuracy_pct": accuracy,
        "avg_prediction_time_ms": round(avg_pred_time, 2),
        "threat_level": threat_level,
    }


def get_attack_breakdown():
    rows = (
        db.session.query(Prediction.predicted_label, func.count(Prediction.id))
        .group_by(Prediction.predicted_label)
        .all()
    )
    return {label: count for label, count in rows}