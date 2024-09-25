from flask import Blueprint, jsonify, request
from sqlalchemy.orm import Session

from app.models import Book, db

books_bp = Blueprint("books", __name__)


@books_bp.route("/books", methods=["POST"])
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


@books_bp.route("/books", methods=["GET"])
def get_all_books():
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


@books_bp.route("/books/<int:book_id>", methods=["GET"])
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
