from datetime import datetime, timedelta, timezone

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

            # 10 days overdue considering BORROWING_PERIOD_DAYS = 7
            borrow_date = datetime.now(timezone.utc) - timedelta(days=17)

            borrow = Borrow(
                user_id=test_user.id, book_id=test_book.id, borrow_date=borrow_date
            )
            db.session.add(borrow)
            db.session.commit()

            access_token = create_access_token(identity=test_user.id)
            client.access_token = access_token

        yield client

        with app.app_context():
            db.drop_all()


def test_calculate_fine_on_return(client):

    # Return the borrowed book with a delay (10 days overdue)
    response = client.post(
        "/books/1/return", headers={"Authorization": f"Bearer {client.access_token}"}
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Book returned successfully"
    assert data["book_id"] == 1
    assert "overdue_fine" in data
    assert data["overdue_fine"] == 20.0

    # Test the fine amount stored in the database
    with client.application.app_context():
        borrow_record = Borrow.query.filter_by(book_id=1).first()
        assert borrow_record.overdue_fine == 20.0
