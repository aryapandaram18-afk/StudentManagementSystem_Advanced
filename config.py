import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


class Config:
    SECRET_KEY = os.environ.get(
        "SECRET_KEY",
        "dev-only-change-this-secret-key",
    )
    DATABASE_PATH = BASE_DIR / "instance" / "students.db"
    TESTING = False