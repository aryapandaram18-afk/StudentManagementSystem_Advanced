
import sqlite3
from functools import wraps

from flask import Blueprint, jsonify, request, session

from app.extensions import get_db

api_bp = Blueprint("api", __name__, url_prefix="/api")


def api_login_required(view):
    """Require login before allowing API access."""

    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if not session.get("user_id"):
            return jsonify({"error": "Authentication required"}), 401

        return view(*args, **kwargs)

    return wrapped_view


def student_to_dict(student):
    """Convert a database row into a JSON-friendly dictionary."""
    return {
        "id": student["id"],
        "name": student["name"],
        "prn": student["prn"],
        "department": student["department"],
        "email": student["email"],
    }


def validate_student_data(data):
    """Check that student fields are present and the email is plausible."""
    fields = ("name", "prn", "department", "email")

    if not all(
        isinstance(data.get(field), str) and data[field].strip()
        for field in fields
    ):
        return "All fields are required."

    email = data["email"].strip()
    if "@" not in email or "." not in email.rsplit("@", 1)[-1]:
        return "Please enter a valid email address."

    return None


@api_bp.route("/students", methods=["GET"])
@api_login_required
def list_students():
    """Return all students."""
    students = get_db().execute(
        """
        SELECT id, name, prn, department, email
        FROM students
        ORDER BY id DESC
        """
    ).fetchall()

    return jsonify({"students": [student_to_dict(s) for s in students]})


@api_bp.route("/students/<int:student_id>", methods=["GET"])
@api_login_required
def get_student(student_id):
    """Return one student by ID."""
    student = get_db().execute(
        """
        SELECT id, name, prn, department, email
        FROM students WHERE id = ?
        """,
        (student_id,),
    ).fetchone()

    if student is None:
        return jsonify({"error": "Student not found"}), 404

    return jsonify(student_to_dict(student))


@api_bp.route("/students", methods=["POST"])
@api_login_required
def create_student():
    """Create a student from a JSON request."""
    data = request.get_json(silent=True) or {}
    error = validate_student_data(data)

    if error:
        return jsonify({"error": error}), 400

    values = (
        data["name"].strip(),
        data["prn"].strip(),
        data["department"].strip(),
        data["email"].strip(),
    )

    database = get_db()

    try:
        cursor = database.execute(
            """
            INSERT INTO students (name, prn, department, email)
            VALUES (?, ?, ?, ?)
            """,
            values,
        )
        database.commit()
    except sqlite3.IntegrityError:
        database.rollback()
        return jsonify({"error": "PRN or email already exists"}), 409

    student = database.execute(
        """
        SELECT id, name, prn, department, email
        FROM students WHERE id = ?
        """,
        (cursor.lastrowid,),
    ).fetchone()

    return jsonify(student_to_dict(student)), 201


@api_bp.route("/students/<int:student_id>", methods=["PUT"])
@api_login_required
def update_student(student_id):
    """Replace a student's details using JSON."""
    data = request.get_json(silent=True) or {}
    error = validate_student_data(data)

    if error:
        return jsonify({"error": error}), 400

    database = get_db()

    existing = database.execute(
        "SELECT id FROM students WHERE id = ?",
        (student_id,),
    ).fetchone()

    if existing is None:
        return jsonify({"error": "Student not found"}), 404

    values = (
        data["name"].strip(),
        data["prn"].strip(),
        data["department"].strip(),
        data["email"].strip(),
        student_id,
    )

    try:
        database.execute(
            """
            UPDATE students
            SET name = ?, prn = ?, department = ?, email = ?
            WHERE id = ?
            """,
            values,
        )
        database.commit()
    except sqlite3.IntegrityError:
        database.rollback()
        return jsonify({"error": "PRN or email already exists"}), 409

    student = database.execute(
        """
        SELECT id, name, prn, department, email
        FROM students WHERE id = ?
        """,
        (student_id,),
    ).fetchone()

    return jsonify(student_to_dict(student))


@api_bp.route("/students/<int:student_id>", methods=["DELETE"])
@api_login_required
def delete_student_api(student_id):
    """Delete a student through the API."""
    database = get_db()

    cursor = database.execute(
        "DELETE FROM students WHERE id = ?",
        (student_id,),
    )
    database.commit()

    if cursor.rowcount == 0:
        return jsonify({"error": "Student not found"}), 404

    return jsonify({"message": "Student deleted successfully"})
