import pytest

from app import create_app, db
from app.models import User


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            test_user = User(username="john_doe", email="john.doe@example.com")
            test_user.set_password("securepassword123")
            db.session.add(test_user)
            db.session.commit()
        yield client
        with app.app_context():
            db.drop_all()


def test_user_login(client):

    login_data = {"email": "john.doe@example.com", "password": "securepassword123"}

    response = client.post("/users/login", json=login_data)

    assert response.status_code == 200
    data = response.get_json()
    assert "access_token" in data

    # Test with incorrect credentials
    invalid_login_data = {"email": "john.doe@example.com", "password": "wrongpassword"}
    response = client.post("/users/login", json=invalid_login_data)
    assert response.status_code == 401
    assert "Invalid credentials" in response.get_json()["error"]
