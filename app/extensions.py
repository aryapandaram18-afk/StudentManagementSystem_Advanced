from flask import current_app, g


def get_db():
    """Return a database connection for the current request."""
    import sqlite3

    if "db" not in g:
        database_path = current_app.config["DATABASE_PATH"]
        database_path.parent.mkdir(parents=True, exist_ok=True)

        connection = sqlite3.connect(database_path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")

        g.db = connection

    return g.db


def close_db(_error=None):
    """Close the database connection when the request ends."""
    database = g.pop("db", None)

    if database is not None:
        database.close()