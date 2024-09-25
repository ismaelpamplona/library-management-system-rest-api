import pytest

from app import create_app, db


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        with app.app_context():
            db.session.remove()
            db.drop_all()
            db.create_all()

        yield client
        with app.app_context():
            db.session.remove()
            db.drop_all()


def test_user_registration(client):
    new_user = {
        "username": "john_doe",
        "email": "john.doe@example.com",
        "password": "securepassword123",
    }

    response = client.post("/users/register", json=new_user)

    assert response.status_code == 201
    data = response.get_json()
    assert data["username"] == "john_doe"
    assert data["email"] == "john.doe@example.com"

    # Check that the password hash is not returned
    assert "password" not in data
    assert "password_hash" not in data

    # Test for an already existing email or username
    response = client.post("/users/register", json=new_user)
    assert response.status_code == 400
    assert "Email or Username already registered" in response.get_json()["error"]
