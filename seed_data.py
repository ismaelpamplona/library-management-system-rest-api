# seed_data.py

from datetime import datetime, timedelta, timezone

from app import create_app, db
from app.models import Book, Borrow, User

app = create_app()

# Use app context
with app.app_context():
    # Drop all existing tables and recreate them
    db.session.remove()
    db.drop_all()
    db.create_all()

    # Create admin user
    admin_user = User(username="admin_user", email="admin@example.com", is_admin=True)
    admin_user.set_password("adminpassword123")
    db.session.add(admin_user)

    # Create regular users
    user1 = User(username="john_doe", email="john.doe@example.com")
    user1.set_password("password123")
    user2 = User(username="jane_doe", email="jane.doe@example.com")
    user2.set_password("password456")
    db.session.add(user1)
    db.session.add(user2)

    # Commit the users to get their IDs
    db.session.commit()

    # Create books
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

    # Commit the books to get their IDs
    db.session.commit()

    # Create borrow records now that user and book IDs are available
    borrow1 = Borrow(
        user_id=user1.id,
        book_id=book1.id,
        borrow_date=datetime.now(timezone.utc) - timedelta(days=10),
        return_date=None,
        overdue_fine=6.0,
    )
    borrow2 = Borrow(
        user_id=user2.id,
        book_id=book2.id,
        borrow_date=datetime.now(timezone.utc) - timedelta(days=5),
        return_date=None,
        overdue_fine=0.0,
    )
    db.session.add(borrow1)
    db.session.add(borrow2)

    # Commit all changes
    db.session.commit()

    print("Database seeded successfully!")
