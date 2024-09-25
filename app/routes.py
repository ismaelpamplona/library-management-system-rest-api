from flask import Blueprint, request, jsonify
from app.models import db, Book

books_bp = Blueprint('books', __name__)

@books_bp.route('/books', methods=['POST'])
def create_book():
    data = request.get_json()

    new_book = Book(
        title=data['title'],
        author=data['author'],
        published_date=data.get('published_date'),
        isbn=data.get('isbn'),
        pages=data.get('pages'),
        cover=data.get('cover'),
        language=data['language']
    )

    db.session.add(new_book)
    db.session.commit()

    return jsonify({
        "id": new_book.id,
        "title": new_book.title,
        "author": new_book.author,
        "published_date": new_book.published_date,
        "isbn": new_book.isbn,
        "pages": new_book.pages,
        "cover": new_book.cover,
        "language": new_book.language
    }), 201
