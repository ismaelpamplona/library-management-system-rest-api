import pytest
from flask_jwt_extended import create_access_token

from app import create_app, db
from app.models import Book, User


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

            test_book = Book(
                title="The Pragmatic Programmer",
                author="Andy Hunt",
                published_date="1999-10-20",
                isbn="9780201616224",
                pages=352,
                cover="https://example.com/pragmatic.jpg",
                language="English",
            )
            db.session.add(test_book)

            db.session.commit()

            access_token = create_access_token(identity=test_user.id)
            client.access_token = (
                access_token  # Attach it to the client for easy access
            )

        yield client

        with app.app_context():
            db.drop_all()


def test_borrow_book(client):

    # Borrow the test book using the authenticated user
    response = client.post(
        "/books/1/borrow", headers={"Authorization": f"Bearer {client.access_token}"}
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Book borrowed successfully"
    assert data["book_id"] == 1
    assert data["user_id"] is not None

    # Test borrowing the same book again, which should not be allowed
    response = client.post(
        "/books/1/borrow", headers={"Authorization": f"Bearer {client.access_token}"}
    )
    assert response.status_code == 400
    assert "Book is already borrowed" in response.get_json()["error"]

    # Test borrowing without authorization
    response = client.post("/books/1/borrow")
    assert response.status_code == 401  # Unauthorized
