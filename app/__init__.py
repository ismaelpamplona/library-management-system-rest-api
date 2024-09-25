from flask import Flask, jsonify
from flask_migrate import Migrate

from config.config import Config

from .models import db
from .routes import books_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    Migrate(app, db)

    app.register_blueprint(books_bp)

    @app.route("/", methods=["GET"])
    def greeting():
        return (
            jsonify(
                {
                    "message": "🚀 Welcome to the Library Management System API! 📚 The API is running smoothly."
                }
            ),
            200,
        )

    return app
