import pytest
from werkzeug.security import generate_password_hash

from app import create_app
from app.extensions import get_db


@pytest.fixture
def app(tmp_path):
    """Create an application with a separate temporary test database."""
    app = create_app(
        {
            "TESTING": True,
            "SECRET_KEY": "test-secret-key",
            "DATABASE_PATH": tmp_path / "test_students.db",
        }
    )

    with app.app_context():
        database = get_db()
        database.execute(
            """
            INSERT INTO users (username, password_hash, role)
            VALUES (?, ?, ?)
            """,
            (
                "testadmin",
                generate_password_hash("TestPass123!"),
                "admin",
            ),
        )
        database.commit()

    yield app


@pytest.fixture
def client(app):
    """Provide a test client for sending HTTP requests."""
    return app.test_client()


@pytest.fixture
def auth_client(client):
    """Provide a client that is already logged in."""
    response = client.post(
        "/login",
        data={
            "username": "testadmin",
            "password": "TestPass123!",
        },
    )
    assert response.status_code == 302
    return client