from flask import Blueprint, render_template

views_bp = Blueprint("views", __name__)


@views_bp.route("/")
@views_bp.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@views_bp.route("/upload")
def upload_page():
    return render_template("upload.html")


@views_bp.route("/live-detection")
def live_detection_page():
    return render_template("live_detection.html")


@views_bp.route("/analytics")
def analytics_page():
    return render_template("analytics.html")


@views_bp.route("/attack-reports")
def attack_reports_page():
    return render_template("attack_reports.html")


@views_bp.route("/model-performance")
def model_performance_page():
    return render_template("model_performance.html")


@views_bp.route("/settings")
def settings_page():
    return render_template("settings.html")