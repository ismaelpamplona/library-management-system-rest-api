from datetime import datetime, timezone

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

db = SQLAlchemy()


class Book(db.Model):
    __tablename__ = "books"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    published_date = db.Column(db.Date, nullable=True)
    isbn = db.Column(db.String(13), unique=True, nullable=True)
    pages = db.Column(db.Integer, nullable=True)
    cover = db.Column(db.String(255), nullable=True)
    language = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"<Book {self.title}>"


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)  # Add this line to the model

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}>"


class Borrow(db.Model):
    __tablename__ = "borrows"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey("books.id"), nullable=False)
    borrow_date = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )
    return_date = db.Column(db.DateTime, nullable=True)
    overdue_fine = db.Column(db.Float, default=0.0)

    user = db.relationship("User", backref="borrows", lazy=True)
    book = db.relationship("Book", backref="borrowed_by", lazy=True)

    def __repr__(self):
        return f"<Borrow user_id={self.user_id}, book_id={self.book_id}, borrow_date={self.borrow_date}, return_date={self.return_date}, overdue_fine={self.overdue_fine}>"
