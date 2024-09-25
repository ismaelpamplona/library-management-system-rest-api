# tests/test_view_all_borrowed_books.py
from datetime import datetime, timezone

import pytest
from flask_jwt_extended import create_access_token

from app import create_app, db
from app.models import Book, Borrow, User


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        with app.app_context():
            db.create_all()

            # Create a test admin user
            admin_user = User(
                username="admin_user", email="admin@example.com", is_admin=True
            )
            admin_user.set_password("adminpassword123")
            db.session.add(admin_user)

            # Create a couple of regular users
            user1 = User(username="john_doe", email="john.doe@example.com")
            user1.set_password("password123")
            user2 = User(username="jane_doe", email="jane.doe@example.com")
            user2.set_password("password456")
            db.session.add(user1)
            db.session.add(user2)
            db.session.commit()

            # Create a few borrowed books for the users
            book1 = Book(
                title="The Pragmatic Programmer",
                author="Andy Hunt",
                published_date="1999-10-20",
                isbn="9780201616224",
                pages=352,
                cover="https://example.com/pragmatic.jpg",
                language="English",
            )
            book2 = Book(
                title="Clean Code",
                author="Robert C. Martin",
                published_date="2008-08-01",
                isbn="9780132350884",
                pages=464,
                cover="https://example.com/clean_code.jpg",
                language="English",
            )
            db.session.add(book1)
            db.session.add(book2)
            db.session.commit()

            borrow1 = Borrow(
                user_id=user1.id,
                book_id=book1.id,
                borrow_date=datetime.now(timezone.utc) - timedelta(days=10),
                return_date=None,
            )
            borrow2 = Borrow(
                user_id=user2.id,
                book_id=book2.id,
                borrow_date=datetime.now(timezone.utc) - timedelta(days=5),
                return_date=None,
            )
            db.session.add(borrow1)
            db.session.add(borrow2)
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


def test_view_all_borrowed_books(client):
    # View all borrowed books as an admin
    response = client.get(
        "/admin/borrowed-books",
        headers={"Authorization": f"Bearer {client.admin_access_token}"},
    )
    assert response.status_code == 200
    data = response.get_json()
    assert len(data["borrowed_books"]) == 2  # Both books should be included
    assert data["borrowed_books"][0]["book_title"] == "The Pragmatic Programmer"
    assert data["borrowed_books"][1]["book_title"] == "Clean Code"

    # Attempt to view all borrowed books as a regular user
    response = client.get(
        "/admin/borrowed-books",
        headers={"Authorization": f"Bearer {client.regular_access_token}"},
    )
    assert response.status_code == 403  # Forbidden

    # Attempt to view all borrowed books without authentication
    response = client.get("/admin/borrowed-books")
    assert response.status_code == 401  # Unauthorized
