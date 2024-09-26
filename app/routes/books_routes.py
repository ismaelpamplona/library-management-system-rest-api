from datetime import datetime, timezone

from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from sqlalchemy.orm import Session

from app.models import Book, Borrow, db

books_bp = Blueprint("books", __name__, url_prefix="/books")

FINE_RATE_PER_DAY = 2.0
BORROWING_PERIOD_DAYS = 7


@books_bp.route("/", methods=["POST"])
def create_book():
    data = request.get_json()

    new_book = Book(
        title=data["title"],
        author=data["author"],
        published_date=data.get("published_date"),
        isbn=data.get("isbn"),
        pages=data.get("pages"),
        cover=data.get("cover"),
        language=data["language"],
    )

    db.session.add(new_book)
    db.session.commit()

    return (
        jsonify(
            {
                "id": new_book.id,
                "title": new_book.title,
                "author": new_book.author,
                "published_date": new_book.published_date,
                "isbn": new_book.isbn,
                "pages": new_book.pages,
                "cover": new_book.cover,
                "language": new_book.language,
            }
        ),
        201,
    )


@books_bp.route("/", methods=["GET"])
def get_all_books():
    try:
        books = Book.query.all()
        return (
            jsonify(
                [
                    {
                        "id": book.id,
                        "title": book.title,
                        "author": book.author,
                        "published_date": book.published_date,
                        "isbn": book.isbn,
                        "pages": book.pages,
                        "cover": book.cover,
                        "language": book.language,
                    }
                    for book in books
                ]
            ),
            200,
        )
    except Exception as e:
        # Log the error to the console
        print(f"Error retrieving books: {e}")
        return jsonify({"error": "An error occurred while retrieving books"}), 500


@books_bp.route("/<int:book_id>", methods=["GET"])
def get_single_book(book_id):
    with Session(db.engine) as session:
        book = session.get(Book, book_id)
        if book is None:
            return jsonify({"error": "Book not found"}), 404

        return (
            jsonify(
                {
                    "id": book.id,
                    "title": book.title,
                    "author": book.author,
                    "published_date": book.published_date,
                    "isbn": book.isbn,
                    "pages": book.pages,
                    "cover": book.cover,
                    "language": book.language,
                }
            ),
            200,
        )


@books_bp.route("/<int:book_id>", methods=["PUT"])
def update_book(book_id):
    with Session(db.engine) as session:
        book = session.get(Book, book_id)
        if book is None:
            return jsonify({"error": "Book not found"}), 404

        data = request.get_json()

        book.title = data.get("title", book.title)
        book.author = data.get("author", book.author)
        book.published_date = data.get("published_date", book.published_date)
        book.isbn = data.get("isbn", book.isbn)
        book.pages = data.get("pages", book.pages)
        book.cover = data.get("cover", book.cover)
        book.language = data.get("language", book.language)

        session.commit()

        return (
            jsonify(
                {
                    "id": book.id,
                    "title": book.title,
                    "author": book.author,
                    "published_date": book.published_date,
                    "isbn": book.isbn,
                    "pages": book.pages,
                    "cover": book.cover,
                    "language": book.language,
                }
            ),
            200,
        )


@books_bp.route("/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    with Session(db.engine) as session:
        book = session.get(Book, book_id)
        if book is None:
            return jsonify({"error": "Book not found"}), 404

        session.delete(book)
        session.commit()

        return "", 204  # Return a 204 No Content response


@books_bp.route("/<int:book_id>/borrow", methods=["POST"])
@jwt_required()
def borrow_book(book_id):
    current_user_id = get_jwt_identity()

    with Session(db.engine) as session:

        book = session.get(Book, book_id)
        if book is None:
            return jsonify({"error": "Book not found"}), 404

        existing_borrow = (
            session.query(Borrow).filter_by(book_id=book_id, return_date=None).first()
        )
        if existing_borrow:
            return jsonify({"error": "Book is already borrowed"}), 400

        new_borrow = Borrow(user_id=current_user_id, book_id=book_id)
        session.add(new_borrow)
        session.commit()

        return (
            jsonify(
                {
                    "message": "Book borrowed successfully",
                    "book_id": new_borrow.book_id,
                    "user_id": new_borrow.user_id,
                    "borrow_date": new_borrow.borrow_date,
                }
            ),
            200,
        )


@books_bp.route("/<int:book_id>/return", methods=["POST"])
@jwt_required()
def return_book(book_id):
    current_user_id = get_jwt_identity()

    with Session(db.engine) as session:
        book = session.get(Book, book_id)
        if book is None:
            return jsonify({"error": "Book not found"}), 404

        borrow = (
            session.query(Borrow)
            .filter_by(book_id=book_id, user_id=current_user_id, return_date=None)
            .first()
        )
        if borrow is None:
            return jsonify({"error": "Book is not currently borrowed"}), 400

        # Ensure borrow.borrow_date is timezone-aware
        if borrow.borrow_date.tzinfo is None:
            borrow.borrow_date = borrow.borrow_date.replace(tzinfo=timezone.utc)

        # Calculate the number of overdue days
        borrow_duration = (datetime.now(timezone.utc) - borrow.borrow_date).days
        overdue_fine = 0.0

        # Adjust fine calculation based on BORROWING_PERIOD_DAYS
        if borrow_duration > BORROWING_PERIOD_DAYS:
            overdue_days = borrow_duration - BORROWING_PERIOD_DAYS
            overdue_fine = overdue_days * FINE_RATE_PER_DAY
            borrow.overdue_fine = overdue_fine

        # Mark the book as returned
        borrow.return_date = datetime.now(timezone.utc)
        session.commit()

        return (
            jsonify(
                {
                    "message": "Book returned successfully",
                    "book_id": borrow.book_id,
                    "return_date": borrow.return_date,
                    "overdue_fine": overdue_fine,
                }
            ),
            200,
        )
