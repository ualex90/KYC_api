from fastapi.testclient import TestClient


def test_read_users_me_for_admin(client: TestClient, admin_token_headers: dict):
    response = client.get("/api/users/me", headers=admin_token_headers)
    assert response.status_code == 200
    assert response.json() == {
        'id': response.json()['id'],
        'email': 'admin@sky.pro',
        'last_name': 'SkyPro',
        'first_name': 'Admin',
        'surname': None,
        'is_active': True,
        'is_staff': True,
        'is_superuser': True,
        'date_joined': response.json()['date_joined'],
    }


def test_read_users_me_for_user(client: TestClient, user1_token_headers: dict):
    response = client.get("/api/users/me", headers=user1_token_headers)
    assert response.status_code == 200
    assert response.json() == {
        'id': response.json()['id'],
        'email': 'ivanov@sky.pro',
        'last_name': 'Иванов',
        'first_name': 'Иван',
        'surname': 'Иванович',
        'is_active': True,
        'is_staff': False,
        'is_superuser': False,
        'date_joined': response.json()['date_joined'],
    }


def test_register_user(client: TestClient, random_user_data: dict):
    response = client.post("/api/users/register", json=random_user_data)
    assert response.status_code == 200


def test_register_user_error400(client: TestClient):
    user_data = {
        'email': 'admin@sky.pro',
        'last_name': 'SkyPro',
        'first_name': 'Admin',
        'surname': None,
        'password': '123qwe',
        'is_active': True,
        'is_staff': True,
        'is_superuser': True,
    }
    response = client.post("/api/users/register", json=user_data)
    assert response.status_code == 400
    assert response.json() == {
        'detail': 'User already exists'
    }


def test_read_users_me(client: TestClient, user1_token_headers):
    response = client.get("/api/users/me", headers=user1_token_headers)
    assert response.status_code == 200
    assert response.json() == {
        'date_joined': response.json()['date_joined'],
        'email': 'ivanov@sky.pro',
        'first_name': 'Иван',
        'id': response.json()['id'],
        'is_active': True,
        'is_staff': False,
        'is_superuser': False,
        'last_name': 'Иванов',
        'surname': 'Иванович'
    }


def test_update_profile_user(client: TestClient, user1_token_headers):
    update_data = {
        'first_name': 'Ванька',
    }
    response = client.patch("/api/users/update", headers=user1_token_headers, json=update_data)
    assert response.status_code == 200
    assert response.json() == {
        'date_joined': response.json()['date_joined'],
        'email': 'ivanov@sky.pro',
        'first_name': 'Ванька',
        'id': response.json()['id'],
        'is_active': True,
        'is_staff': False,
        'is_superuser': False,
        'last_name': 'Иванов',
        'surname': 'Иванович'
    }


def test_delete_user(client: TestClient, user1_token_headers):
    response = client.delete("/api/users/delete", headers=user1_token_headers)
    assert response.status_code == 200
    assert response.json() == {'detail': 'deleted'}
