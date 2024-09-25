# implement_fine_management_for_overdue_books (Issue)

- [x] Set up fine-related attributes in the `Borrow` model:
  - [x] Add an `overdue_fine` column to the `Borrow` model.
  - [x] Create migration scripts for the fine-related changes using Flask-Migrate.
- [x] Implement logic to calculate overdue fines:
  - [x] Write a failing test for fine calculation upon returning a book.
  - [x] Implement the fine calculation logic based on the number of overdue days.
  - [x] Make the test pass.
- [x] Implement endpoint to view outstanding fines for a user:
  - [x] Write a failing test for viewing outstanding fines.
  - [x] Implement the logic to retrieve and display outstanding fines.
  - [x] Make the test pass.
- [x] Implement endpoint to pay fines:
  - [x] Write a failing test for fine payment.
  - [x] Implement the fine payment logic.
  - [x] Make the test pass.
- [x] Test all fine management functionalities to ensure they work correctly.

```bash
================================ test session starts =================================
platform linux -- Python 3.12.6, pytest-8.3.3, pluggy-1.5.0
rootdir: /usr/src/app
configfile: pyproject.toml
plugins: cov-5.0.0
collected 18 items

tests/test_book_creation.py .                                                  [  5%]
tests/test_book_deletion.py .                                                  [ 11%]
tests/test_book_retrieval.py ...                                               [ 27%]
tests/test_book_update.py .                                                    [ 33%]
tests/test_borrow_book.py .                                                    [ 38%]
tests/test_fine_calculation.py .                                               [ 44%]
tests/test_greeting.py .                                                       [ 50%]
tests/test_pay_fine.py .                                                       [ 55%]
tests/test_return_book.py .                                                    [ 61%]
tests/test_user_deletion.py .                                                  [ 66%]
tests/test_user_login.py .                                                     [ 72%]
tests/test_user_profile.py .                                                   [ 77%]
tests/test_user_registration.py .                                              [ 83%]
tests/test_user_update.py .                                                    [ 88%]
tests/test_view_borrowed_books.py .                                            [ 94%]
tests/test_view_outstanding_fines.py .                                         [100%]

================================= 18 passed in 6.86s =================================
```
