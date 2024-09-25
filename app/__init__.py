# app/__init__.py
from flask import Flask
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

def create_app():
    app = Flask(__name__)

    # Configure Flask settings from environment variables
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['DATABASE_URL'] = os.getenv('DATABASE_URL')

    @app.route('/')
    def hello_world():
        return "<h1>Hello, World!</h1>"

    return app
