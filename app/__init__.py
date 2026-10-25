from flask import Flask, redirect, session, url_for

from app.api.routes import api_bp
from app.auth.routes import auth_bp
from app.database.models import init_db
from app.extensions import close_db, get_db
from app.students.routes import students_bp
from config import Config


def create_app(test_config=None):
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config.from_object(Config)

    if test_config is not None:
        app.config.update(test_config)

    app.teardown_appcontext(close_db)
    app.register_blueprint(auth_bp)
    app.register_blueprint(students_bp)
    app.register_blueprint(api_bp)

    @app.route("/")
    def index():
        if session.get("user_id"):
            return redirect(url_for("students.dashboard"))
        return redirect(url_for("auth.login"))

    with app.app_context():
        init_db(get_db())

    return app