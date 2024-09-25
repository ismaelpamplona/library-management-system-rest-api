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

            test_user = User(username="john_doe", email="john.doe@example.com")
            test_user.set_password("securepassword123")
            db.session.add(test_user)

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
                user_id=test_user.id,
                book_id=book1.id,
                borrow_date=datetime.now(timezone.utc),
            )
            borrow2 = Borrow(
                user_id=test_user.id,
                book_id=book2.id,
                borrow_date=datetime.now(timezone.utc),
            )
            db.session.add(borrow1)
            db.session.add(borrow2)
            db.session.commit()

            access_token = create_access_token(identity=test_user.id)
            client.access_token = access_token

        yield client

        with app.app_context():
            db.drop_all()


def test_view_borrowed_books(client):

    # View all borrowed books for the authenticated user
    response = client.get(
        "/users/borrowed-books",
        headers={"Authorization": f"Bearer {client.access_token}"},
    )
    assert response.status_code == 200
    data = response.get_json()["borrowed_books"]
    assert len(data) == 2
    assert data[0]["title"] == "The Pragmatic Programmer"
    assert data[1]["title"] == "Clean Code"

    # Test viewing borrowed books without authorization
    response = client.get("/users/borrowed-books")
    assert response.status_code == 401  # Unauthorized
