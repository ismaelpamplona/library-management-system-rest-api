from flask import Flask
from .models import db
from config.config import Config

def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)

    @app.route('/')
    def hello_world():
        return "<h1>Hello, World!</h1>"

    return app
