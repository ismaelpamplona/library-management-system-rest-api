from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token
from sqlalchemy.orm import Session

from app.models import User, db

users_bp = Blueprint("users", __name__)


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
