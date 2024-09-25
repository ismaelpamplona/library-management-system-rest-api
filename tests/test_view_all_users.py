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
            db.create_all()

            admin_user = User(
                username="admin_user", email="admin@example.com", is_admin=True
            )
            admin_user.set_password("adminpassword123")
            db.session.add(admin_user)

            user1 = User(username="john_doe", email="john.doe@example.com")
            user1.set_password("password123")
            user2 = User(username="jane_doe", email="jane.doe@example.com")
            user2.set_password("password456")
            db.session.add(user1)
            db.session.add(user2)
            db.session.commit()

            # Generate an access token for the admin user
            admin_access_token = create_access_token(identity=admin_user.id)
            client.admin_access_token = admin_access_token

            # Generate an access token for a regular user
            regular_access_token = create_access_token(identity=user1.id)
            client.regular_access_token = regular_access_token

        yield client

        with app.app_context():
            db.drop_all()


def test_view_all_users(client):
    # View all users as an admin
    response = client.get(
        "/admin/users", headers={"Authorization": f"Bearer {client.admin_access_token}"}
    )
    assert response.status_code == 200
    data = response.get_json()
    assert len(data["users"]) == 3  # Including the admin user
    assert any(user["username"] == "john_doe" for user in data["users"])
    assert any(user["username"] == "jane_doe" for user in data["users"])

    # Attempt to view all users as a regular user
    response = client.get(
        "/admin/users",
        headers={"Authorization": f"Bearer {client.regular_access_token}"},
    )
    assert response.status_code == 403  # Forbidden

    # Attempt to view all users without authentication
    response = client.get("/admin/users")
    assert response.status_code == 401  # Unauthorized
