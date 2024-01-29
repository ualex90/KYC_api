from fastapi.testclient import TestClient


def test_get_token(client: TestClient):
    data = {
        "email": "admin@sky.pro",
        "password": "123qwe"
    }
    resource = client.post('/api/auth/token', json=data)
    assert resource.status_code == 200
    assert resource.json() == {
        "access_token": resource.json()["access_token"],
        "token_type": "Bearer"
    }


def test_get_token_error401(client: TestClient):
    data = {
        "email": "nologin@sky.pro",
        "password": "12345"
    }
    resource = client.post('/api/auth/token', json=data)
    assert resource.status_code == 401
    assert resource.json() == {
        "detail": "Wrong login details",
    }


def test_decode_token_error(client: TestClient):
    token_headers = {"Authorization": f"Bearer qweasdzxcrtyfghvbnuiojklm"}
    resource = client.get('/api/users/me', headers=token_headers)
    assert resource.status_code == 401
    assert resource.json() == {
        "detail": "Could not validate credentials",
    }

# def test_get_token_swagger(client: TestClient):
#     data = {
#         "username": "admin@sky.pro",
#         "password": "123qwe"
#     }
#     resource = client.post('/token', json=data)
#     # assert resource.status_code == 200
#     assert resource.json() == {
#         "access_token": resource.json()["access_token"],
#         "token_type": "bearer"
#     }
#
#
# def test_get_token_swagger_error401(client: TestClient):
#     data = {
#         "username": "nologin@sky.pro",
#         "password": "12345"
#     }
#     resource = client.post('/token', json=data)
#     assert resource.status_code == 401
#     assert resource.json() == {
#         "detail": "Wrong login details",
#     }
