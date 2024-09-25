# implement_book_management (Issue)

- [x] Set up the Book model with SQLAlchemy.
- [x] Create database migration scripts using Flask-Migrate.
- [x] Implement book creation endpoint:
  - [x] Write a failing test for book creation.
  - [x] Implement the book creation logic.
  - [x] Make the test pass.
- [x] Implement book retrieval endpoints:
  - [x] Write failing tests for retrieving single and multiple books.
  - [x] Implement the retrieval logic.
  - [x] Make the tests pass.
- [x] Implement book updating endpoint:
  - [x] Write a failing test for updating a book.
  - [x] Implement the update logic.
  - [x] Make the test pass.
- [x] Implement book deletion endpoint:
  - [x] Write a failing test for deleting a book.
  - [x] Implement the deletion logic.
  - [x] Make the test pass.
- [x] Test all book management functionalities to ensure they work correctly.

```bash
$ docker-compose -f compose.dev.yml exec flask_app poetry run pytest
================================ test session starts =================================
platform linux -- Python 3.12.6, pytest-8.3.3, pluggy-1.5.0
rootdir: /usr/src/app
configfile: pyproject.toml
plugins: cov-5.0.0
collected 7 items

tests/test_book_creation.py .                                                  [ 14%]
tests/test_book_deletion.py .                                                  [ 28%]
tests/test_book_retrieval.py ...                                               [ 71%]
tests/test_book_update.py .                                                    [ 85%]
tests/test_greeting.py .                                                       [100%]

================================= 7 passed in 0.85s ==================================
(library-management-system-rest-api-py3.12)
```
