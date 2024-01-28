from fastapi.testclient import TestClient


def test_get_list_users(client: TestClient, admin_token_headers):
    response = client.get("/api/users/list", headers=admin_token_headers)
    assert response.status_code == 200
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


def test_get_list_users_error403(client: TestClient, user1_token_headers):
    response = client.get("/api/users/list", headers=user1_token_headers)
    assert response.status_code == 403
    assert response.json() == {'detail': "The user doesn't have enough privileges"}


def test_get_detail_user(client: TestClient, admin_token_headers):
    response = client.get("/api/users/1", headers=admin_token_headers)
    assert response.status_code == 200
    assert response.json() == {
        'id': 1,
        'email': 'admin@sky.pro',
        'last_name': 'SkyPro',
        'first_name': 'Admin',
        'surname': None,
        'is_active': True,
        'is_staff': True,
        'is_superuser': True,
        'date_joined': response.json()['date_joined'],
        'last_login': None,
        'comments': None,
    }


def test_get_detail_user_error403(client: TestClient, user1_token_headers):
    response = client.get("/api/users/1", headers=user1_token_headers)
    assert response.status_code == 403
    assert response.json() == {'detail': "The user doesn't have enough privileges"}


def test_get_detail_user_error404(client: TestClient, admin_token_headers):
    response = client.get("/api/users/100", headers=admin_token_headers)
    assert response.status_code == 404
    assert response.json() == {
        'detail': "User not found"
    }
