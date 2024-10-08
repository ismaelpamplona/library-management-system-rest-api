from flasgger import Swagger
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

from app.routes import admin_bp, books_bp, users_bp
from config.config import Config

from .models import db

swagger = Swagger(template_file="../config/swagger.yml")


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    Migrate(app, db)
    JWTManager(app)

    app.register_blueprint(books_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(admin_bp)

    # Initialize Swagger
    swagger.init_app(app)

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
