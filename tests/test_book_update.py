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


def test_update_book(client):

    updated_data = {
        "title": "The Pragmatic Programmer - Updated",
        "author": "Andy Hunt & Dave Thomas",
        "published_date": "1999-10-30",
        "isbn": "9780201616224",
        "pages": 400,
        "cover": "https://example.com/pragmatic_updated.jpg",
        "language": "English",
    }

    response = client.put("/books/1", json=updated_data)

    assert response.status_code == 200
    data = response.get_json()
    assert data["title"] == "The Pragmatic Programmer - Updated"
    assert data["author"] == "Andy Hunt & Dave Thomas"
    assert data["pages"] == 400

    response = client.put("/books/999", json=updated_data)
    assert response.status_code == 404
