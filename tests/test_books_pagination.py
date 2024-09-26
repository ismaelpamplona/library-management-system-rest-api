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

            # Add multiple books for pagination testing
            books_data = [
                {
                    "title": f"Book {i}",
                    "author": "Author",
                    "published_date": "2020-01-01",
                    "isbn": f"978020161622{i}",
                    "pages": 100 + i,
                    "cover": "https://example.com/cover.jpg",
                    "language": "English",
                }
                for i in range(1, 21)
            ]

            for book_data in books_data:
                book = Book(**book_data)
                db.session.add(book)

            db.session.commit()
        yield client
        with app.app_context():
            db.session.remove()
            db.drop_all()


def test_books_pagination(client):
    # Test the first page with 5 books per page
    response = client.get("/books?page=1&per_page=5")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 5
    assert data[0]["title"] == "Book 1"
    assert data[-1]["title"] == "Book 5"

    # Test the second page with 5 books per page
    response = client.get("/books?page=2&per_page=5")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 5
    assert data[0]["title"] == "Book 6"
    assert data[-1]["title"] == "Book 10"

    # Test an empty page (out of range)
    response = client.get("/books?page=5&per_page=5")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 0
