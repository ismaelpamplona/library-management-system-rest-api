from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Book(db.Model):
    __tablename__ = 'books'

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
