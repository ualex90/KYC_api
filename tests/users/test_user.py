from fastapi.testclient import TestClient


def test_register_user(client: TestClient, user1_data: dict):
    response = client.post("/api/users/register", json=user1_data)
    assert response.status_code == 200


def test_register_user2(client: TestClient, user2_data: dict):
    response = client.post("/api/users/register", json=user2_data)
    assert response.status_code == 200
