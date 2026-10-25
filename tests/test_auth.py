def test_login_page_loads(client):
    response = client.get("/login")

    assert response.status_code == 200
    assert b"Student Management System" in response.data


def test_login_rejects_empty_credentials(client):
    response = client.post(
        "/login",
        data={"username": "", "password": ""},
    )

    assert response.status_code == 400


def test_login_rejects_wrong_password(client):
    response = client.post(
        "/login",
        data={
            "username": "testadmin",
            "password": "WrongPassword",
        },
    )

    assert response.status_code == 401


def test_login_accepts_valid_credentials(client):
    response = client.post(
        "/login",
        data={
            "username": "testadmin",
            "password": "TestPass123!",
        },
    )

    assert response.status_code == 302
    assert response.headers["Location"].endswith("/dashboard")


def test_dashboard_requires_login(client):
    response = client.get("/dashboard")

    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


def test_logout_clears_session(auth_client):
    response = auth_client.post("/logout")

    assert response.status_code == 302

    dashboard_response = auth_client.get("/dashboard")
    assert dashboard_response.status_code == 302
    assert "/login" in dashboard_response.headers["Location"]