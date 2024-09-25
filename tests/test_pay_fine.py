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
            db.session.remove()
            db.drop_all()
            db.create_all()

            test_user = User(username="john_doe", email="john.doe@example.com")
            test_user.set_password("securepassword123")
            db.session.add(test_user)

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

            borrow = Borrow(
                user_id=test_user.id,
                book_id=book.id,
                borrow_date=datetime.now(timezone.utc)
                - timedelta(days=17),  # 10 days overdue
                return_date=datetime.now(timezone.utc) - timedelta(days=1),
                overdue_fine=20.0,  # 10 days * $2/day
            )
            db.session.add(borrow)
            db.session.commit()

            access_token = create_access_token(identity=test_user.id)
            client.access_token = access_token

        yield client

        with app.app_context():
            db.session.remove()
            db.drop_all()


def test_pay_fine(client):
    # Pay the fine for the overdue book
    response = client.post(
        "/users/pay-fine",
        json={"book_id": 1},
        headers={"Authorization": f"Bearer {client.access_token}"},
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Fine paid successfully"
    assert data["book_id"] == 1
    assert data["paid_amount"] == 20.0

    # Check that the fine is marked as paid in the database
    with client.application.app_context():
        borrow_record = Borrow.query.filter_by(book_id=1).first()
        assert borrow_record.overdue_fine == 0.0

    # Test paying a fine for a book without any outstanding fine
    response = client.post(
        "/users/pay-fine",
        json={"book_id": 1},
        headers={"Authorization": f"Bearer {client.access_token}"},
    )
    assert response.status_code == 400
    assert "No outstanding fine" in response.get_json()["error"]

    # Test paying a fine without authorization
    response = client.post("/users/pay-fine", json={"book_id": 1})
    assert response.status_code == 401  # Unauthorized
