from datetime import datetime
from app import db


class Prediction(db.Model):
    __tablename__ = "predictions"

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    features = db.Column(db.JSON, nullable=False)

    predicted_class_id = db.Column(db.Integer, nullable=False)
    predicted_label = db.Column(db.String(64), nullable=False)
    confidence = db.Column(db.Float, nullable=False)

    true_label = db.Column(db.String(64), nullable=True)
    batch_id = db.Column(db.String(64), nullable=True, index=True)
    prediction_time_ms = db.Column(db.Float, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "created_at": self.created_at.isoformat(),
            "predicted_class_id": self.predicted_class_id,
            "predicted_label": self.predicted_label,
            "confidence": round(self.confidence, 4),
            "true_label": self.true_label,
            "batch_id": self.batch_id,
            "prediction_time_ms": self.prediction_time_ms,
        }