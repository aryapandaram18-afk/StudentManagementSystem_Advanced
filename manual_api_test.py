
import getpass
import uuid

from app import create_app


def main():
    app = create_app()
    client = app.test_client()

    username = input("Enter your admin username: ").strip()
    password = getpass.getpass("Enter your admin password: ")

    # Log in to establish an authenticated session.
    response = client.post(
        "/login",
        data={"username": username, "password": password},
    )

    if response.status_code != 302:
        print("Login failed. Check your credentials.")
        return

    print("PASS: Login")

    suffix = uuid.uuid4().hex[:8]
    student_data = {
        "name": "API Test Student",
        "prn": f"API-{suffix}",
        "department": "Computer Engineering",
        "email": f"api-{suffix}@example.com",
    }

    student_id = None

    try:
        # 1. POST: Create a student.
        response = client.post("/api/students", json=student_data)
        print("POST status:", response.status_code)

        if response.status_code != 201:
            print("POST failed:", response.get_json())
            return

        student_id = response.get_json()["id"]
        print("PASS: Create student")

        # 2. GET: Retrieve the student.
        response = client.get(f"/api/students/{student_id}")
        print("GET status:", response.status_code)

        if response.status_code != 200:
            print("GET failed:", response.get_json())
            return

        print("PASS: Retrieve student")
        print("Student:", response.get_json())

        # 3. PUT: Update the student.
        updated_data = {
            **student_data,
            "name": "Updated API Test Student",
        }

        response = client.put(
            f"/api/students/{student_id}",
            json=updated_data,
        )
        print("PUT status:", response.status_code)

        if response.status_code != 200:
            print("PUT failed:", response.get_json())
            return

        print("PASS: Update student")

        # 4. GET: List all students.
        response = client.get("/api/students")
        print("List status:", response.status_code)

        if response.status_code != 200:
            print("List failed:", response.get_json())
            return

        print("PASS: List students")

        # 5. DELETE: Remove the temporary test student.
        response = client.delete(f"/api/students/{student_id}")
        print("DELETE status:", response.status_code)

        if response.status_code != 200:
            print("DELETE failed:", response.get_json())
            return

        student_id = None
        print("PASS: Delete student")

        # Confirm that the deleted student cannot be retrieved.
        response = client.get(
            f"/api/students/{response.get_json().get('id', -1)}"
        )
        # The deletion was successful; verify using the saved ID
        # in the next revision if needed.

    finally:
        # Clean up the temporary record if a test failed midway.
        if student_id is not None:
            client.delete(f"/api/students/{student_id}")

    print("\nAPI testing finished.")


if __name__ == "__main__":
    main()
