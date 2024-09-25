import pytest
from flask import Flask, jsonify

from app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_greeting(client):
    response = client.get("/")

    expected = {
        "message": "🚀 Welcome to the Library Management System API! 📚 The API is running smoothly."
    }

    assert response.status_code == 200
    assert response.get_json() == expected
