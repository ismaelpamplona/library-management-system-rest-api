import pytest

from app import create_app, db
from app.models import Book


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        with app.app_context():
            db.create_all()

            book = Book(
                title="The Pragmatic Programmer",
                author="Andy Hunt",
                published_date="1999-10-20",
                isbn="9780201616224",
                pages=352,
                cover="https://example.com/pragmatic.jpg",
                language="English",
            )
            db.session.add(book)
            db.session.commit()
        yield client
        with app.app_context():
            db.drop_all()


def test_delete_book(client):

    response = client.delete("/books/1")

    assert response.status_code == 204  # No Content

    response = client.get("/books/1")
    assert response.status_code == 404  # Not Found

    response = client.delete("/books/999")
    assert response.status_code == 404
