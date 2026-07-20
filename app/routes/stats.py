from flask import Blueprint, jsonify
from app.services import stats_service

stats_bp = Blueprint("stats", __name__)


@stats_bp.route("/stats/summary", methods=["GET"])
def stats_summary():
    return jsonify(stats_service.get_summary_stats()), 200


@stats_bp.route("/stats/breakdown", methods=["GET"])
def stats_breakdown():
    return jsonify(stats_service.get_attack_breakdown()), 200