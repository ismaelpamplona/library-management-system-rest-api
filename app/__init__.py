from flask import Flask
from dotenv import load_dotenv
import os

load_dotenv()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['DATABASE_URL'] = os.getenv('DATABASE_URL')

    @app.route('/')
    def hello_world():
        return "Hello, World!"

    return app
