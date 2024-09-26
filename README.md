# Library Management System REST API

🐍📚 A Library Management System REST API using Python, Flask, and PostgreSQL. It follows OOP and TDD paradigms, providing features like user management, book handling, and borrowing/returning with 🔑 JWT-based authentication. The system is 🐳 containerized with Docker for easy setup and deployment.

## 🚀 Features

- User Registration and Authentication (JWT)
- Admin and User Role Management
- Book Borrowing and Returning
- Fine Calculation for Overdue Books
- View and Manage User Profiles
- Admin Management of Users and Borrow Records
- View Borrowed Books and Outstanding Fines

## 📚 Technologies Used

- Python 3.12
- Flask
- Flask-JWT-Extended
- Flask-SQLAlchemy
- Flask-Migrate
- PostgreSQL
- Docker and Docker Compose
- Poetry for Dependency Management
- pytest for Testing

## 📋 Improvements

The following enhancements are planned to be implemented in future iterations:

1. **Implement Pagination for User and Book Endpoints**: Improve API performance and user experience by implementing pagination on endpoints that return lists of users or books.

2. **Add Sorting and Filtering Options to Book and User Endpoints**: Enhance the searchability and organization of data by adding options to sort and filter the books and user lists based on attributes such as name, author, email, etc.

3. **Create Password Reset Functionality**: Implement a secure password reset mechanism allowing users to reset their passwords using an email-based token system.

4. **Implement Search Functionality for Books**: Add the ability to search for books by title, author, or ISBN to improve the user experience in finding specific books.

5. **Enhance User Profile with Additional Attributes**: Expand the user profile with more details such as bio, profile picture, contact information, etc.

6. **Implement Global Error Handling and Input Validation**: Ensure consistent error handling and input validation across the entire application, improving robustness and providing clear error messages.

## 📑 Issue Management

This application uses [ripissue](https://github.com/cwnt-io/ripissue) to manage issues with Git and the filesystem.

## 🐳 Running the Application with Docker

### 🔧 Configuration

The application reads environment variables from the .env file. Make sure to create one with the following keys:

```bash
FLASK_ENV=development
FLASK_APP=app
SECRET_KEY=your_secret_key_here

POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=library_management
POSTGRES_PORT=5432
POSTGRES_HOST=postgres

JWT_SECRET_KEY=your_jwt_secret_key_here
JWT_ACCESS_TOKEN_EXPIRES=3600  # Optional
JWT_REFRESH_TOKEN_EXPIRES=86400  # Optional
```

Ensure you have Docker and Docker Compose installed on your machine. You can start the application with:

```bash
docker compose -f compose.dev.yml up --build
```

### Database Setup

After starting the containers, you need to perform the following steps to set up the database:

#### Run Migrations

Run the following command to apply the latest migrations and create the necessary tables:

```bash
docker compose -f compose.dev.yml exec flask_app poetry run flask db upgrade
```

If the migrations are successful, the tables will be created automatically in your database.

### Apply Seed Data (Optional)

To populate the database with sample data, you can run the seed script using the following command:

```bash
docker compose -f compose.dev.yml exec flask_app poetry run python seed_data.py
```

### 🧪 Testing the Application with Docker

The application follows a **Test-Driven Development (TDD)** paradigm. All features are thoroughly tested using `pytest`, ensuring that each functionality works as expected. To run the tests, execute:

```bash
docker compose -f compose.dev.yml exec flask_app poetry run pytest
```

## Access Swagger Documentation

Once everything is set up, you can access the Swagger API documentation at:

```
http://localhost:5000/apidocs/
```

## 💡 Contributing

Contributions are welcome! Please feel free to submit a Pull Request for any enhancements, bug fixes, or documentation improvements.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.
