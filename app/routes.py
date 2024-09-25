from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token
from sqlalchemy.orm import Session

from app.models import Book, User, db

books_bp = Blueprint("books", __name__)
users_bp = Blueprint("users", __name__)


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


@books_bp.route("/books/<int:book_id>", methods=["PUT"])
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


@books_bp.route("/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    with Session(db.engine) as session:
        book = session.get(Book, book_id)
        if book is None:
            return jsonify({"error": "Book not found"}), 404

        session.delete(book)
        session.commit()

        return "", 204  # Return a 204 No Content response


@users_bp.route("/register", methods=["POST"])
def register_user():
    data = request.get_json()

    # Check if the email or username already exists
    with Session(db.engine) as session:
        existing_user = (
            session.query(User)
            .filter((User.email == data["email"]) | (User.username == data["username"]))
            .first()
        )
        if existing_user:
            return jsonify({"error": "Email or Username already registered"}), 400

        new_user = User(username=data["username"], email=data["email"])
        new_user.set_password(data["password"])  # Hash the password

        session.add(new_user)
        session.commit()

        return (
            jsonify(
                {
                    "id": new_user.id,
                    "username": new_user.username,
                    "email": new_user.email,
                }
            ),
            201,
        )


@users_bp.route("/login", methods=["POST"])
def login_user():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    with Session(db.engine) as session:
        user = session.query(User).filter_by(email=email).first()
        if user is None or not user.check_password(password):
            return jsonify({"error": "Invalid credentials"}), 401

        # Create an access token using Flask-JWT-Extended
        access_token = create_access_token(identity=user.id)

        return jsonify({"access_token": access_token}), 200
