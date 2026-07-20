from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()


def create_app(config_class="app.config.Config"):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)

    from app.routes.views import views_bp
    from app.routes.predict import predict_bp
    from app.routes.upload import upload_bp
    from app.routes.stats import stats_bp
    from app.routes.history import history_bp

    app.register_blueprint(views_bp)
    app.register_blueprint(predict_bp)
    app.register_blueprint(upload_bp)
    app.register_blueprint(stats_bp, url_prefix="/api")
    app.register_blueprint(history_bp, url_prefix="/api")

    return app