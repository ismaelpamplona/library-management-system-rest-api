from flask import Blueprint, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from sqlalchemy.orm import Session

from app.models import User, db

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
