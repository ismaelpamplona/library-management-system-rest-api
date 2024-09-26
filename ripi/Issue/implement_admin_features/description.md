# implement_admin_features (Issue)

- [x] Implement endpoint for viewing all users:
  - [x] Write a failing test for viewing all users.
  - [x] Implement the logic to retrieve all users.
  - [x] Make the test pass.
- [x] Implement endpoint for viewing all borrowed books by all users:
  - [x] Write a failing test for viewing all borrowed books.
  - [x] Implement the logic to retrieve all borrowed books.
  - [x] Make the test pass.
- [x] Implement endpoint for deleting any user's borrow record:
  - [x] Write a failing test for deleting a user's borrow record.
  - [x] Implement the deletion logic.
  - [x] Make the test pass.
- [x] Implement admin authentication and authorization checks:
  - [x] Write a failing test to ensure only admins can access admin endpoints.
  - [x] Implement the admin role check logic.
  - [x] Make the test pass.
- [x] Test all admin functionalities to ensure they work correctly.

```bash

================================ test session starts =================================
platform linux -- Python 3.12.6, pytest-8.3.3, pluggy-1.5.0
rootdir: /usr/src/app
configfile: pyproject.toml
plugins: cov-5.0.0
collected 24 items

tests/test_admin_auth.py .                                                     [  4%]
tests/test_book_creation.py .                                                  [  8%]
tests/test_book_deletion.py .                                                  [ 12%]
tests/test_book_retrieval.py ...                                               [ 25%]
tests/test_book_update.py .                                                    [ 29%]
tests/test_borrow_book.py .                                                    [ 33%]
tests/test_delete_borrow_record.py ...                                         [ 45%]
tests/test_fine_calculation.py .                                               [ 50%]
tests/test_greeting.py .                                                       [ 54%]
tests/test_pay_fine.py .                                                       [ 58%]
tests/test_return_book.py .                                                    [ 62%]
tests/test_user_deletion.py .                                                  [ 66%]
tests/test_user_login.py .                                                     [ 70%]
tests/test_user_profile.py .                                                   [ 75%]
tests/test_user_registration.py .                                              [ 79%]
tests/test_user_update.py .                                                    [ 83%]
tests/test_view_all_borrowed_books.py .                                        [ 87%]
tests/test_view_all_users.py .                                                 [ 91%]
tests/test_view_borrowed_books.py .                                            [ 95%]
tests/test_view_outstanding_fines.py .                                         [100%]

================================ 24 passed in 10.11s =================================
```
