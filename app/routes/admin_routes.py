from flask import Blueprint, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from sqlalchemy.orm import Session

from app.models import Book, Borrow, User, db

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.route("/users", methods=["GET"])
@jwt_required()
def view_all_users():
    current_user_id = get_jwt_identity()

    with Session(db.engine) as session:
        current_user = session.get(User, current_user_id)
        if not current_user or not getattr(current_user, "is_admin", False):
            return jsonify({"error": "Access forbidden: Admins only"}), 403

        # Retrieve all users
        all_users = session.query(User).all()
        users_list = [
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "is_admin": user.is_admin,
            }
            for user in all_users
        ]

        return jsonify({"users": users_list}), 200


@admin_bp.route("/borrowed-books", methods=["GET"])
@jwt_required()
def view_all_borrowed_books():
    current_user_id = get_jwt_identity()

    with Session(db.engine) as session:
        # Check if the current user is an admin
        current_user = session.get(User, current_user_id)
        if not current_user or not getattr(current_user, "is_admin", False):
            return jsonify({"error": "Access forbidden: Admins only"}), 403

        # Retrieve all borrowed books
        borrowed_books = (
            session.query(Borrow)
            .join(Book, Borrow.book_id == Book.id)
            .join(User, Borrow.user_id == User.id)
            .all()
        )

        borrowed_books_list = [
            {
                "borrow_id": borrow.id,
                "user_id": borrow.user_id,
                "username": borrow.user.username,
                "book_id": borrow.book_id,
                "book_title": borrow.book.title,
                "borrow_date": borrow.borrow_date,
                "return_date": borrow.return_date,
                "overdue_fine": borrow.overdue_fine,
            }
            for borrow in borrowed_books
        ]

        return jsonify({"borrowed_books": borrowed_books_list}), 200


@admin_bp.route("/borrow/<int:borrow_id>", methods=["DELETE"])
@jwt_required()
def delete_borrow_record(borrow_id):
    current_user_id = get_jwt_identity()

    with Session(db.engine) as session:
        current_user = session.get(User, current_user_id)

        if not current_user or not getattr(current_user, "is_admin", False):
            return jsonify({"error": "Forbidden: Admins only"}), 403

        borrow_record = session.get(Borrow, borrow_id)

        if not borrow_record:
            return jsonify({"error": "Borrow record not found"}), 404

        session.delete(borrow_record)
        session.commit()

    return "", 204  # No content
