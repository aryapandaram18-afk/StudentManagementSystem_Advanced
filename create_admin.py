import getpass

from werkzeug.security import generate_password_hash

from app import create_app
from app.extensions import get_db


def main():
    app = create_app()

    with app.app_context():
        username = input("Enter admin username: ").strip()
        password = getpass.getpass("Enter admin password: ")

        if not username or not password:
            print("Username and password cannot be empty.")
            return

        database = get_db()

        try:
            database.execute(
                """
                INSERT INTO users (username, password_hash, role)
                VALUES (?, ?, ?)
                """,
                (username, generate_password_hash(password), "admin"),
            )
            database.commit()
            print(f"Admin account '{username}' created successfully.")
        except Exception as error:
            database.rollback()
            print(f"Could not create admin account: {error}")


if __name__ == "__main__":
    main()