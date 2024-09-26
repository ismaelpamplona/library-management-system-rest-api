from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from sqlalchemy.orm import Session

from app.models import Book, Borrow, User, db

users_bp = Blueprint("users", __name__, url_prefix="/users")


@users_bp.route("/register", methods=["POST"])
def register_user():
    """
    Register a new user
    ---
    tags:
      - Users
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              username:
                type: string
              email:
                type: string
              password:
                type: string
            required:
              - username
              - email
              - password
    responses:
      201:
        description: User registered successfully
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/User'
      400:
        description: "Email or Username already registered"
    """
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
    """
    User login
    ---
    tags:
      - Users
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              email:
                type: string
              password:
                type: string
            required:
              - email
              - password
    responses:
      200:
        description: User logged in successfully
        content:
          application/json:
            schema:
              type: object
              properties:
                access_token:
                  type: string
      401:
        description: Invalid credentials
    """
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
    """
    Get user profile
    ---
    tags:
      - Users
    security:
      - BearerAuth: []
    responses:
      200:
        description: User profile retrieved successfully
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/User'
      404:
        description: User not found
    """
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
    """
    Update user profile
    ---
    tags:
      - Users
    security:
      - BearerAuth: []
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              username:
                type: string
              email:
                type: string
    responses:
      200:
        description: User profile updated successfully
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/User'
      404:
        description: User not found
    """
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
    """
    Delete user profile
    ---
    tags:
      - Users
    security:
      - BearerAuth: []
    responses:
      204:
        description: User profile deleted successfully
      404:
        description: User not found
    """
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
    """
    Get all borrowed books by the user
    ---
    tags:
      - Users
    security:
      - BearerAuth: []
    responses:
      200:
        description: List of borrowed books
        content:
          application/json:
            schema:
              type: array
              items:
                $ref: '#/components/schemas/BorrowedBook'
    """
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
    """
    View all outstanding fines for the user
    ---
    tags:
      - Users
    security:
      - BearerAuth: []
    responses:
      200:
        description: List of outstanding fines
        content:
          application/json:
            schema:
              type: object
              properties:
                total_outstanding_fines:
                  type: number
                fines:
                  type: array
                  items:
                    $ref: '#/components/schemas/Fine'
    """
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


@users_bp.route("/pay-fine", methods=["POST"])
@jwt_required()
def pay_fine():
    """
    Pay outstanding fine for a specific book
    ---
    tags:
      - Users
    security:
      - BearerAuth: []
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              book_id:
                type: integer
            required:
              - book_id
    responses:
      200:
        description: Fine paid successfully
      404:
        description: Borrow record not found
      400:
        description: No outstanding fine for this book
    """
    current_user_id = get_jwt_identity()
    data = request.get_json()
    book_id = data.get("book_id")

    if not book_id:
        return jsonify({"error": "Book ID is required"}), 400

    with Session(db.engine) as session:
        # Find the borrow record for this user and book
        borrow_record = (
            session.query(Borrow)
            .filter_by(user_id=current_user_id, book_id=book_id)
            .first()
        )

        if borrow_record is None:
            return jsonify({"error": "Borrow record not found"}), 404

        if borrow_record.overdue_fine == 0.0:
            return jsonify({"error": "No outstanding fine for this book"}), 400

        # Mark the fine as paid
        paid_amount = borrow_record.overdue_fine
        borrow_record.overdue_fine = 0.0
        session.commit()

        return (
            jsonify(
                {
                    "message": "Fine paid successfully",
                    "book_id": book_id,
                    "paid_amount": paid_amount,
                }
            ),
            200,
        )
