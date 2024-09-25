from .admin_routes import admin_bp
from .books_routes import books_bp
from .users_routes import users_bp

__all__ = ["books_bp", "users_bp", "admin_bp"]
