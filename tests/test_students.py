
from app.extensions import get_db


def test_add_student(auth_client):
    """A logged-in user can add a student."""
    response = auth_client.post(
        "/students/add",
        data={
            "name": "Test Student",
            "prn": "CE1001",
            "department": "Computer Engineering",
            "email": "test1001@example.com",
        },
    )

    assert response.status_code == 302

    dashboard = auth_client.get("/dashboard")
    assert dashboard.status_code == 200
    assert b"Test Student" in dashboard.data


def test_add_student_rejects_empty_fields(auth_client):
    """Student details cannot be empty."""
    response = auth_client.post(
        "/students/add",
        data={
            "name": "",
            "prn": "CE1002",
            "department": "Computer Engineering",
            "email": "test1002@example.com",
        },
    )

    assert response.status_code == 400


def test_add_student_rejects_duplicate_prn(auth_client):
    """Two students cannot have the same PRN."""
    student_data = {
        "name": "First Student",
        "prn": "CE2001",
        "department": "Computer Engineering",
        "email": "first2001@example.com",
    }

    first_response = auth_client.post(
        "/students/add",
        data=student_data,
    )
    assert first_response.status_code == 302

    duplicate_response = auth_client.post(
        "/students/add",
        data={
            **student_data,
            "name": "Second Student",
            "email": "second2001@example.com",
        },
    )

    assert duplicate_response.status_code == 409


def test_edit_student(auth_client):
    """A logged-in user can update a student."""
    auth_client.post(
        "/students/add",
        data={
            "name": "Original Student",
            "prn": "CE3001",
            "department": "Computer Engineering",
            "email": "original3001@example.com",
        },
    )

    with auth_client.application.app_context():
        student = get_db().execute(
            "SELECT id FROM students WHERE prn = ?",
            ("CE3001",),
        ).fetchone()

    student_id = student["id"]

    response = auth_client.post(
        f"/students/{student_id}/edit",
        data={
            "name": "Updated Student",
            "prn": "CE3001",
            "department": "Information Technology",
            "email": "updated3001@example.com",
        },
    )

    assert response.status_code == 302

    dashboard = auth_client.get("/dashboard")
    assert b"Updated Student" in dashboard.data
    assert b"Information Technology" in dashboard.data


def test_delete_student(auth_client):
    """A logged-in user can delete a student."""
    auth_client.post(
        "/students/add",
        data={
            "name": "Student To Delete",
            "prn": "CE4001",
            "department": "Computer Engineering",
            "email": "delete4001@example.com",
        },
    )

    with auth_client.application.app_context():
        student = get_db().execute(
            "SELECT id FROM students WHERE prn = ?",
            ("CE4001",),
        ).fetchone()

    student_id = student["id"]

    response = auth_client.post(
        f"/students/{student_id}/delete"
    )

    assert response.status_code == 302

    dashboard = auth_client.get("/dashboard")
    assert b"Student To Delete" not in dashboard.data
