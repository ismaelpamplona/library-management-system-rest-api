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

            regular_user = User(username="john_doe", email="john.doe@example.com")
            regular_user.set_password("password123")
            db.session.add(regular_user)
            db.session.commit()

            admin_access_token = create_access_token(identity=admin_user.id)
            client.admin_access_token = admin_access_token

            regular_access_token = create_access_token(identity=regular_user.id)
            client.regular_access_token = regular_access_token

        yield client

        with app.app_context():
            db.drop_all()


def test_admin_access(client):
    # Attempt to access an admin route as an admin user
    response = client.delete(
        "/admin/borrow/1",
        headers={"Authorization": f"Bearer {client.admin_access_token}"},
    )
    assert response.status_code != 403  # Ensure the admin has access

    # Attempt to access an admin route as a regular user
    response = client.delete(
        "/admin/borrow/1",
        headers={"Authorization": f"Bearer {client.regular_access_token}"},
    )
    assert response.status_code == 403  # Ensure access is forbidden for non-admins
