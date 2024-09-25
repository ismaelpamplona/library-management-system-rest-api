import pytest

from app import create_app, db


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()


def test_create_book(client):

    new_book = {
        "title": "The Pragmatic Programmer",
        "author": "Andy Hunt",
        "published_date": "1999-10-20",
        "isbn": "9780201616224",
        "pages": 352,
        "cover": "https://example.com/pragmatic.jpg",
        "language": "English",
    }

    response = client.post("/books", json=new_book)

    assert response.status_code == 201
    assert response.json["title"] == "The Pragmatic Programmer"
    assert response.json["author"] == "Andy Hunt"
