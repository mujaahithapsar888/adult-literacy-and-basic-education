def test_health_check(client):
    response = client.get("/")
    assert response.status_code == 200

def test_user_registration(client):
    response = client.post("/auth/register", json={
        "email": "testuser@edudash.com",
        "password": "strongpassword123",
        "role": "Student"
    })
    assert response.status_code == 200
    assert response.json()["email"] == "testuser@edudash.com"

def test_user_login(client):
    response = client.post("/auth/login", data={
        "username": "testuser@edudash.com",
        "password": "strongpassword123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "refresh_token" in response.json()
