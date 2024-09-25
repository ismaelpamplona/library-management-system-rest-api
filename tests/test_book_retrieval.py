import pytest

from app import create_app, db
from app.models import Book


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        with app.app_context():
            db.session.remove()
            db.drop_all()
            db.create_all()

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
                cover="https://example.com/cleancode.jpg",
                language="English",
            )

            db.session.add(book1)
            db.session.add(book2)
            db.session.commit()
        yield client
        with app.app_context():
            db.session.remove()
            db.drop_all()


def test_get_all_books(client):
    response = client.get("/books/")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 2
    assert data[0]["title"] == "The Pragmatic Programmer"
    assert data[1]["title"] == "Clean Code"


def test_get_single_book(client):
    response = client.get("/books/1")
    assert response.status_code == 200
    data = response.get_json()
    assert data["title"] == "The Pragmatic Programmer"
    assert data["author"] == "Andy Hunt"


def test_get_non_existent_book(client):
    response = client.get("/books/999")
    assert response.status_code == 404
