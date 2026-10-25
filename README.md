
![Student Management System CI](https://github.com/aryapandaram18-afk/StudentManagementSystem_Advanced/actions/workflows/ci.yml/badge.svg)

# Online Student Management System

A web application for managing student records using Flask, SQLite, and Python.

## Features

- Admin and staff login
- Add, view, edit, and delete student records
- REST API for student operations
- Automated tests using pytest
- Code quality checks using Ruff
- Continuous Integration using GitHub Actions

## Setup

Install the dependencies:

```bash
python -m pip install -r requirements.txt
```

Run the application:

```bash
python app.py
```

Open http://127.0.0.1:5000/login in your browser.

## Run Tests

```bash
python -m pytest --cov=app --cov-report=term-missing --cov-fail-under=80
```

## Code Quality

```bash
python -m ruff check app.py config.py app tests
```

## CI Workflow

GitHub Actions automatically runs lint checks, Python compilation, automated tests, and the minimum 80% code coverage check when changes are pushed or pull requests are opened.
