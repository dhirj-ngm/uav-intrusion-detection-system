from flask import Blueprint, jsonify, request
from app.models.prediction import Prediction

history_bp = Blueprint("history", __name__)


@history_bp.route("/predictions", methods=["GET"])
def list_predictions():
    limit = min(int(request.args.get("limit", 50)), 500)
    offset = int(request.args.get("offset", 0))
    batch_id = request.args.get("batch_id")
    label = request.args.get("label")

    query = Prediction.query.order_by(Prediction.created_at.desc())

    if batch_id:
        query = query.filter_by(batch_id=batch_id)
    if label:
        query = query.filter_by(predicted_label=label)

    total = query.count()
    rows = query.offset(offset).limit(limit).all()

    return jsonify({
        "total": total,
        "limit": limit,
        "offset": offset,
        "predictions": [row.to_dict() for row in rows],
    }), 200