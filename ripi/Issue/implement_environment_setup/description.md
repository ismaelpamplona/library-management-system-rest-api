# implement_environment_setup (Issue)

- [x] Create a new Python virtual environment with poetry and activate it.
- [x] Install all the dependencies needed:
  - [x] Main Dependencies
    - [x] Flask
    - [x] Flask-RESTful
    - [x] SQLAlchemy
    - [x] Flask-SQLAlchemy
    - [x] Flask-JWT-Extended
    - [x] Flask-Migrate
    - [x] psycopg2-binary
    - [x] Marshmallow
  - [x] Development Dependencies
    - [x] Pytest - For testing
    - [x] Flake8 - For code linting
    - [x] Black - For code formatting
    - [x] isort - For sorting imports
    - [x] pytest-cov - For test coverage reports
    - [x] mypy - For static type checking
- [x] Add `.gitignore` file for your Python and Poetry-based project.
- [x] Set up a basic project structure with folders: `app`, `tests`, and `config`.
- [x] Create a `compose.yml` to manage PostgreSQL service.
- [x] Set up a `.env` file for environment variables.
- [x] Configure Flask to read from the `.env` file and create a basic "Hello, World!" route.
- [x] Set up Docker with a `Dockerfile.dev` for the Flask app.
- [x] Create a `compose.yml` to manage Flask service.
- [x] Test the Docker setup to ensure both the Flask app and PostgreSQL start correctly.
- [x] Write a simple test using Pytest to check the "Hello, World!" endpoint.
- [x] Make the first successful test pass using TDD.

```bash
$ docker compose -f compose.dev.yml exec flask_app poetry run pytest
================================ test session starts =================================
platform linux -- Python 3.12.6, pytest-8.3.3, pluggy-1.5.0
rootdir: /usr/src/app
configfile: pyproject.toml
plugins: cov-5.0.0
collected 1 item

tests/test_hello_world.py .                                                    [100%]

================================= 1 passed in 0.14s ==================================
```
