from functools import wraps

from flask import Blueprint, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from sqlalchemy.orm import Session

from app.models import Book, Borrow, User, db

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


def admin_required(fn):
    """Decorator to ensure the user is an admin"""

    @wraps(fn)  # This preserves the original function's identity
    @jwt_required()
    def wrapper(*args, **kwargs):
        current_user_id = get_jwt_identity()

        with Session(db.engine) as session:
            current_user = session.get(User, current_user_id)

            if not current_user or not getattr(current_user, "is_admin", False):
                return jsonify({"error": "Forbidden: Admins only"}), 403

            return fn(*args, **kwargs)

    return wrapper


@admin_bp.route("/users", methods=["GET"])
@admin_required
def view_all_users():
    """
    Get all users
    ---
    tags:
      - Admin
    security:
      - BearerAuth: []
    responses:
      200:
        description: List of all users
        content:
          application/json:
            schema:
              type: object
              properties:
                users:
                  type: array
                  items:
                    type: object
                    properties:
                      id:
                        type: integer
                      username:
                        type: string
                      email:
                        type: string
                      is_admin:
                        type: boolean
      403:
        description: "Access forbidden: Admins only"
    """
    with Session(db.engine) as session:
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
@admin_required
def view_all_borrowed_books():
    """
    Get all borrowed books
    ---
    tags:
      - Admin
    security:
      - BearerAuth: []
    responses:
      200:
        description: List of all borrowed books
        content:
          application/json:
            schema:
              type: object
              properties:
                borrowed_books:
                  type: array
                  items:
                    type: object
                    properties:
                      borrow_id:
                        type: integer
                      user_id:
                        type: integer
                      username:
                        type: string
                      book_id:
                        type: integer
                      book_title:
                        type: string
                      borrow_date:
                        type: string
                        format: date
                      return_date:
                        type: string
                        format: date
                      overdue_fine:
                        type: number
      403:
        description: "Access forbidden: Admins only"
    """
    with Session(db.engine) as session:
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
@admin_required
def delete_borrow_record(borrow_id):
    """
    Delete a borrow record
    ---
    tags:
      - Admin
    security:
      - BearerAuth: []
    parameters:
      - name: borrow_id
        in: path
        required: true
        description: The ID of the borrow record to delete
        schema:
          type: integer
    responses:
      204:
        description: Borrow record deleted successfully
      404:
        description: "Borrow record not found"
      403:
        description: "Access forbidden: Admins only"
    """
    with Session(db.engine) as session:
        borrow_record = session.get(Borrow, borrow_id)

        if not borrow_record:
            return jsonify({"error": "Borrow record not found"}), 404

        session.delete(borrow_record)
        session.commit()

    return "", 204  # No content
