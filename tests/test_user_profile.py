import pytest
from flask_jwt_extended import create_access_token

from app import create_app, db
from app.models import User


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        with app.app_context():
            db.session.remove()
            db.drop_all()
            db.create_all()

            test_user = User(username="john_doe", email="john.doe@example.com")
            test_user.set_password("securepassword123")
            db.session.add(test_user)
            db.session.commit()

            access_token = create_access_token(identity=test_user.id)
            client.access_token = (
                access_token  # Attach it to the client for easy access
            )

        yield client

        with app.app_context():
            db.session.remove()
            db.drop_all()


def test_user_profile_retrieval(client):

    # Retrieve user profile with authorization header
    response = client.get(
        "/users/profile", headers={"Authorization": f"Bearer {client.access_token}"}
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["username"] == "john_doe"
    assert data["email"] == "john.doe@example.com"

    # Test retrieving a profile without authorization
    response = client.get("/users/profile")
    assert response.status_code == 401  # Unauthorized
