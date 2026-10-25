
import sqlite3
from functools import wraps

from flask import (
    Blueprint,
    abort,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from app.extensions import get_db

students_bp = Blueprint("students", __name__)


def login_required(view):
    """Allow access only to authenticated users."""

    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if not session.get("user_id"):
            return redirect(url_for("auth.login"))

        return view(*args, **kwargs)

    return wrapped_view


@students_bp.route("/dashboard")
@login_required
def dashboard():
    """Display all student records."""
    students = get_db().execute(
        """
        SELECT id, name, prn, department, email
        FROM students
        ORDER BY id DESC
        """
    ).fetchall()

    return render_template("dashboard.html", students=students)


@students_bp.route("/students/add", methods=["GET", "POST"])
@login_required
def add_student():
    """Add a new student record."""
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        prn = request.form.get("prn", "").strip()
        department = request.form.get("department", "").strip()
        email = request.form.get("email", "").strip()

        if not all([name, prn, department, email]):
            flash("All fields are required.", "error")
            return render_template("student_form.html"), 400

        if "@" not in email or "." not in email.rsplit("@", 1)[-1]:
            flash("Please enter a valid email address.", "error")
            return render_template("student_form.html"), 400

        database = get_db()

        try:
            database.execute(
                """
                INSERT INTO students (name, prn, department, email)
                VALUES (?, ?, ?, ?)
                """,
                (name, prn, department, email),
            )
            database.commit()

        except sqlite3.IntegrityError:
            database.rollback()
            flash(
                "This PRN or email address already exists.",
                "error",
            )
            return render_template("student_form.html"), 409

        flash("Student added successfully!", "success")
        return redirect(url_for("students.dashboard"))

    return render_template("student_form.html")


@students_bp.route(
    "/students/<int:student_id>/edit",
    methods=["GET", "POST"],
)
@login_required
def edit_student(student_id):
    """Edit an existing student record."""
    database = get_db()

    student = database.execute(
        """
        SELECT id, name, prn, department, email
        FROM students
        WHERE id = ?
        """,
        (student_id,),
    ).fetchone()

    if student is None:
        abort(404)

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        prn = request.form.get("prn", "").strip()
        department = request.form.get("department", "").strip()
        email = request.form.get("email", "").strip()

        if not all([name, prn, department, email]):
            flash("All fields are required.", "error")
            return render_template(
                "edit_student.html", student=student
            ), 400

        if "@" not in email or "." not in email.rsplit("@", 1)[-1]:
            flash("Please enter a valid email address.", "error")
            return render_template(
                "edit_student.html", student=student
            ), 400

        try:
            database.execute(
                """
                UPDATE students
                SET name = ?, prn = ?, department = ?, email = ?
                WHERE id = ?
                """,
                (name, prn, department, email, student_id),
            )
            database.commit()

        except sqlite3.IntegrityError:
            database.rollback()
            flash(
                "This PRN or email address already exists.",
                "error",
            )
            return render_template(
                "edit_student.html", student=student
            ), 409

        flash("Student updated successfully!", "success")
        return redirect(url_for("students.dashboard"))

    return render_template("edit_student.html", student=student)

@students_bp.route(
    "/students/<int:student_id>/delete",
    methods=["POST"],
)
@login_required
def delete_student(student_id):
    """Delete an existing student record."""
    database = get_db()

    student = database.execute(
        "SELECT id FROM students WHERE id = ?",
        (student_id,),
    ).fetchone()

    if student is None:
        abort(404)

    database.execute(
        "DELETE FROM students WHERE id = ?",
        (student_id,),
    )
    database.commit()

    flash("Student deleted successfully!", "success")
    return redirect(url_for("students.dashboard"))
