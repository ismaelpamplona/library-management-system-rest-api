from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from sqlalchemy.orm import Session

from app.models import Book, Borrow, User, db

users_bp = Blueprint("users", __name__, url_prefix="/users")


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


@users_bp.route("/profile", methods=["GET"])
@jwt_required()
def get_user_profile():
    current_user_id = get_jwt_identity()

    with Session(db.engine) as session:
        user = session.get(User, current_user_id)
        if user is None:
            return jsonify({"error": "User not found"}), 404

        return (
            jsonify({"id": user.id, "username": user.username, "email": user.email}),
            200,
        )


@users_bp.route("/profile", methods=["PUT"])
@jwt_required()
def update_user_profile():
    current_user_id = get_jwt_identity()
    data = request.get_json()

    with Session(db.engine) as session:
        user = session.get(User, current_user_id)
        if user is None:
            return jsonify({"error": "User not found"}), 404

        # Update user details
        user.username = data.get("username", user.username)
        user.email = data.get("email", user.email)

        session.commit()

        return (
            jsonify({"id": user.id, "username": user.username, "email": user.email}),
            200,
        )


@users_bp.route("/profile", methods=["DELETE"])
@jwt_required()
def delete_user_profile():
    current_user_id = get_jwt_identity()

    with Session(db.engine) as session:
        user = session.get(User, current_user_id)
        if user is None:
            return jsonify({"error": "User not found"}), 404

        session.delete(user)
        session.commit()

        return "", 204  # Return a 204 No Content response


@users_bp.route("/borrowed-books", methods=["GET"])
@jwt_required()
def get_borrowed_books():
    current_user_id = get_jwt_identity()

    with Session(db.engine) as session:
        borrowed_books = (
            session.query(Borrow)
            .join(Book, Borrow.book_id == Book.id)
            .filter(Borrow.user_id == current_user_id, Borrow.return_date == None)
            .all()
        )

        books_list = [
            {
                "book_id": borrow.book.id,
                "title": borrow.book.title,
                "author": borrow.book.author,
                "borrow_date": borrow.borrow_date,
            }
            for borrow in borrowed_books
        ]

        return jsonify({"borrowed_books": books_list}), 200


@users_bp.route("/outstanding-fines", methods=["GET"])
@jwt_required()
def view_outstanding_fines():
    current_user_id = get_jwt_identity()

    with Session(db.engine) as session:
        # Query all outstanding fines for the user
        outstanding_fines = (
            session.query(Borrow)
            .join(Book, Borrow.book_id == Book.id)
            .filter(Borrow.user_id == current_user_id, Borrow.overdue_fine > 0)
            .all()
        )

        total_outstanding_fines = sum(
            borrow.overdue_fine for borrow in outstanding_fines
        )
        fines_list = [
            {
                "book_title": borrow.book.title,
                "fine_amount": borrow.overdue_fine,
                "borrow_date": borrow.borrow_date,
                "return_date": borrow.return_date,
            }
            for borrow in outstanding_fines
        ]

        return (
            jsonify(
                {
                    "total_outstanding_fines": total_outstanding_fines,
                    "fines": fines_list,
                }
            ),
            200,
        )
