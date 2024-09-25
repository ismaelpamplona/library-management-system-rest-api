# implement_borrowing_and_returning_books (Issue)

- [x] Set up the Borrow model with SQLAlchemy to track borrowing transactions:
  - [x] Define the model with relationships to User and Book.
  - [x] Create migration scripts for the Borrow model using Flask-Migrate.
- [x] Implement book borrowing endpoint:
  - [x] Write a failing test for borrowing a book.
  - [x] Implement the borrowing logic.
  - [x] Make the test pass.
- [x] Implement book returning endpoint:
  - [x] Write a failing test for returning a book.
  - [x] Implement the returning logic.
  - [x] Make the test pass.
- [x] Implement endpoint to view all borrowed books for a user:
  - [x] Write a failing test for viewing borrowed books.
  - [x] Implement the logic to fetch borrowed books.
  - [x] Make the test pass.
- [x] Test all borrowing and returning functionalities to ensure they work correctly.

```bash
======================= test session starts ========================
platform linux -- Python 3.12.6, pytest-8.3.3, pluggy-1.5.0
rootdir: /usr/src/app
configfile: pyproject.toml
plugins: cov-5.0.0
collected 15 items

tests/test_book_creation.py .                                [  6%]
tests/test_book_deletion.py .                                [ 13%]
tests/test_book_retrieval.py ...                             [ 33%]
tests/test_book_update.py .                                  [ 40%]
tests/test_borrow_book.py .                                  [ 46%]
tests/test_greeting.py .                                     [ 53%]
tests/test_return_book.py .                                  [ 60%]
tests/test_user_deletion.py .                                [ 66%]
tests/test_user_login.py .                                   [ 73%]
tests/test_user_profile.py .                                 [ 80%]
tests/test_user_registration.py .                            [ 86%]
tests/test_user_update.py .                                  [ 93%]
tests/test_view_borrowed_books.py .                          [100%]

======================== 15 passed in 2.97s ========================
```
