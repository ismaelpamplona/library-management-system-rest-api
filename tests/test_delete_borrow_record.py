from datetime import datetime, timedelta, timezone

import pytest
from flask_jwt_extended import create_access_token
from sqlalchemy.orm import Session

from app import create_app, db
from app.models import Book, Borrow, User


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        with app.app_context():
            db.session.remove()  # Clear any existing session
            db.drop_all()
            db.create_all()

            # Create an admin user
            admin_user = User(
                username="admin_user", email="admin@example.com", is_admin=True
            )
            admin_user.set_password("adminpassword123")
            db.session.add(admin_user)

            # Create a regular user
            user1 = User(username="john_doe", email="john.doe@example.com")
            user1.set_password("password123")
            db.session.add(user1)

            # Create a book with all required fields
            book1 = Book(
                title="Example Book",
                author="Author",
                isbn="1234567890",
                pages=100,
                cover="https://example.com/cover.jpg",
                language="English",
                published_date="2020-01-01",
            )
            db.session.add(book1)
            db.session.commit()

            # Create a borrow record for the regular user
            borrow_record = Borrow(
                user_id=user1.id,
                book_id=book1.id,
                borrow_date=datetime.now(timezone.utc) - timedelta(days=5),
            )
            db.session.add(borrow_record)
            db.session.commit()

            client.borrow_id = borrow_record.id

            # Generate access tokens
            admin_access_token = create_access_token(identity=admin_user.id)
            client.admin_access_token = admin_access_token

            regular_access_token = create_access_token(identity=user1.id)
            client.regular_access_token = regular_access_token

        yield client

        with app.app_context():
            db.session.remove()  # Clean up the session properly
            db.drop_all()  # Ensure tables are dropped


def test_delete_borrow_record_as_admin(client):

    borrow_id = client.borrow_id
    response = client.delete(
        f"/admin/borrow/{borrow_id}",
        headers={"Authorization": f"Bearer {client.admin_access_token}"},
    )
    assert response.status_code == 204  # No content

    with client.application.app_context():
        with Session(db.engine) as session:
            borrow_record = session.get(Borrow, borrow_id)
            assert borrow_record is None


def test_delete_borrow_record_as_regular_user(client):

    borrow_id = client.borrow_id
    response = client.delete(
        f"/admin/borrow/{borrow_id}",
        headers={"Authorization": f"Bearer {client.regular_access_token}"},
    )
    assert response.status_code == 403  # Forbidden


def test_delete_nonexistent_borrow_record(client):
    response = client.delete(
        "/admin/borrow/9999",
        headers={"Authorization": f"Bearer {client.admin_access_token}"},
    )
    assert response.status_code == 404  # Not found
