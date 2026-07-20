import os
import uuid
import pandas as pd
from flask import Blueprint, request, jsonify, current_app

upload_bp = Blueprint("upload", __name__)
ALLOWED_EXTENSIONS = {"csv"}


def _allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@upload_bp.route("/upload", methods=["POST"])
def upload_dataset():
    if "file" not in request.files:
        return jsonify({"success": False, "message": "No file part in request"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"success": False, "message": "No file selected"}), 400

    if not _allowed_file(file.filename):
        return jsonify({"success": False, "message": "Only .csv files are supported"}), 400

    os.makedirs(current_app.config["UPLOAD_FOLDER"], exist_ok=True)

    batch_id = uuid.uuid4().hex[:12]
    save_path = os.path.join(current_app.config["UPLOAD_FOLDER"], f"{batch_id}.csv")
    file.save(save_path)

    try:
        df = pd.read_csv(save_path)
    except Exception as e:
        return jsonify({"success": False, "message": f"Could not read CSV: {str(e)}"}), 400

    return jsonify({
        "success": True,
        "filename": batch_id,          # opaque id the frontend just echoes back on /predict
        "rows": len(df),
        "columns": list(df.columns),
        "preview": df.head(10).to_dict(orient="records"),
    }), 201