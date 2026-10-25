
def sample_student():
    """Return sample student data for API tests."""
    return {
        "name": "API Test Student",
        "prn": "API1001",
        "department": "Computer Engineering",
        "email": "api1001@example.com",
    }


def test_api_requires_login(client):
    response = client.get("/api/students")

    assert response.status_code == 401
    assert response.get_json()["error"] == "Authentication required"


def test_list_students(auth_client):
    response = auth_client.get("/api/students")

    assert response.status_code == 200
    assert response.get_json()["students"] == []


def test_create_student(auth_client):
    response = auth_client.post(
        "/api/students",
        json=sample_student(),
    )

    assert response.status_code == 201
    assert response.get_json()["name"] == "API Test Student"
    assert response.get_json()["prn"] == "API1001"


def test_create_student_rejects_missing_fields(auth_client):
    response = auth_client.post(
        "/api/students",
        json={"name": "Incomplete Student"},
    )

    assert response.status_code == 400


def test_create_student_rejects_duplicate_prn(auth_client):
    auth_client.post(
        "/api/students",
        json=sample_student(),
    )

    duplicate = sample_student()
    duplicate["name"] = "Another Student"
    duplicate["email"] = "another@example.com"

    response = auth_client.post("/api/students", json=duplicate)

    assert response.status_code == 409


def test_get_single_student(auth_client):
    created = auth_client.post(
        "/api/students",
        json=sample_student(),
    )
    student_id = created.get_json()["id"]

    response = auth_client.get(f"/api/students/{student_id}")

    assert response.status_code == 200
    assert response.get_json()["id"] == student_id


def test_get_missing_student(auth_client):
    response = auth_client.get("/api/students/999999")

    assert response.status_code == 404


def test_update_student(auth_client):
    created = auth_client.post(
        "/api/students",
        json=sample_student(),
    )
    student_id = created.get_json()["id"]

    updated_data = {
        **sample_student(),
        "name": "Updated API Student",
        "department": "Information Technology",
        "email": "updated_api@example.com",
    }

    response = auth_client.put(
        f"/api/students/{student_id}",
        json=updated_data,
    )

    assert response.status_code == 200
    assert response.get_json()["name"] == "Updated API Student"
    assert response.get_json()["department"] == "Information Technology"


def test_update_missing_student(auth_client):
    response = auth_client.put(
        "/api/students/999999",
        json=sample_student(),
    )

    assert response.status_code == 404


def test_delete_student(auth_client):
    created = auth_client.post(
        "/api/students",
        json=sample_student(),
    )
    student_id = created.get_json()["id"]

    response = auth_client.delete(f"/api/students/{student_id}")

    assert response.status_code == 200
    assert response.get_json()["message"] == "Student deleted successfully"

    missing = auth_client.get(f"/api/students/{student_id}")
    assert missing.status_code == 404


def test_delete_missing_student(auth_client):
    response = auth_client.delete("/api/students/999999")

    assert response.status_code == 404
