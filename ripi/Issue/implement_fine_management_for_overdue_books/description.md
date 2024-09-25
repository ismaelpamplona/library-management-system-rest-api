# implement_fine_management_for_overdue_books (Issue)

- [x] Set up fine-related attributes in the `Borrow` model:
  - [x] Add an `overdue_fine` column to the `Borrow` model.
  - [x] Create migration scripts for the fine-related changes using Flask-Migrate.
- [ ] Implement logic to calculate overdue fines:
  - [ ] Write a failing test for fine calculation upon returning a book.
  - [ ] Implement the fine calculation logic based on the number of overdue days.
  - [ ] Make the test pass.
- [ ] Implement endpoint to view outstanding fines for a user:
  - [ ] Write a failing test for viewing outstanding fines.
  - [ ] Implement the logic to retrieve and display outstanding fines.
  - [ ] Make the test pass.
- [ ] Implement endpoint to pay fines:
  - [ ] Write a failing test for fine payment.
  - [ ] Implement the fine payment logic.
  - [ ] Make the test pass.
- [ ] Test all fine management functionalities to ensure they work correctly.
