import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-only-change-me")

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "postgresql://postgres:postgres@localhost:5432/uav_ids"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MODEL_PATH = os.environ.get(
        "MODEL_PATH",
        os.path.join(BASE_DIR, "app", "ml_models", "stacking_pipeline.joblib")
    )

    UPLOAD_FOLDER = os.environ.get(
        "UPLOAD_FOLDER",
        os.path.join(BASE_DIR, "uploads")
    )
    MAX_CONTENT_LENGTH = 25 * 1024 * 1024

    class_names = {
        0: "Blackhole Attack",
        1: "Flooding Attack",
        2: "Normal Traffic",
        3: "Sybil Attack",
        4: "Wormhole Attack",
    }