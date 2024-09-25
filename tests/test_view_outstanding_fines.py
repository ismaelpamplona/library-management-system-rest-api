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
                borrow_date=datetime.now(timezone.utc)
                - timedelta(days=17),  # 10 days overdue
                return_date=datetime.now(timezone.utc) - timedelta(days=1),
                overdue_fine=20.0,  # 10 days * $2/day
            )
            borrow2 = Borrow(
                user_id=test_user.id,
                book_id=book2.id,
                borrow_date=datetime.now(timezone.utc)
                - timedelta(days=14),  # 7 days overdue
                return_date=None,
                overdue_fine=14.0,  # 7 days * $2/day
            )
            db.session.add(borrow1)
            db.session.add(borrow2)
            db.session.commit()

            access_token = create_access_token(identity=test_user.id)
            client.access_token = access_token

        yield client

        with app.app_context():
            db.session.remove()
            db.drop_all()


def test_view_outstanding_fines(client):
    # View all outstanding fines for the authenticated user
    response = client.get(
        "/users/outstanding-fines",
        headers={"Authorization": f"Bearer {client.access_token}"},
    )

    assert response.status_code == 200
    data = response.get_json()
    assert "total_outstanding_fines" in data
    assert data["total_outstanding_fines"] == 34.0  # $20 + $14
    assert len(data["fines"]) == 2
    assert data["fines"][0]["book_title"] == "The Pragmatic Programmer"
    assert data["fines"][0]["fine_amount"] == 20.0
    assert data["fines"][1]["book_title"] == "Clean Code"
    assert data["fines"][1]["fine_amount"] == 14.0

    # Test viewing fines without authorization
    response = client.get("/users/outstanding-fines")
    assert response.status_code == 401  # Unauthorized
