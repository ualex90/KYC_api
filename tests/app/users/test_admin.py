from fastapi.testclient import TestClient


def test_get_users(client: TestClient, admin_token_headers):
    response = client.get("/api/users/list", headers=admin_token_headers)
    assert response.json() == {
        "items": [
            {
                "id": 1,
                "email": "admin@sky.pro",
                "is_active": True
            },
            {
                "id": 2,
                "email": "ivanov@sky.pro",
                "is_active": True
            },
            {
                "id": 3,
                "email": "petrov@sky.pro",
                "is_active": True
            },
        ],
        "total": 3,
        "page": 1,
        "size": 50,
        "pages": 1
    }
