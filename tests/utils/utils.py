from fastapi.testclient import TestClient

test_users = [
    {
        'email': 'admin@sky.pro',
        'last_name': 'SkyPro',
        'first_name': 'Admin',
        'surname': None,
        'password': '123qwe',
        'is_active': True,
        'is_staff': True,
        'is_superuser': True,
    },
    {
        'email': 'ivanov@sky.pro',
        'last_name': 'Иванов',
        'first_name': 'Иван',
        'surname': 'Иванович',
        'password': '123qwe',
        'is_active': True,
        'is_staff': False,
        'is_superuser': False,
    },
    {
        'email': 'petrov@sky.pro',
        'last_name': 'Петров',
        'first_name': 'Петр',
        'surname': 'Петрович',
        'password': '123qwe',
        'is_active': True,
        'is_staff': False,
        'is_superuser': False,
    },
    {
        'email': 'sidorov@sky.pro',
        'last_name': 'Сидоров',
        'first_name': 'Сидр',
        'surname': 'Сидорович',
        'password': '123qwe',
        'is_active': True,
        'is_staff': False,
        'is_superuser': False,
    }
]


def register_test_users(client: TestClient):
    for user_data in test_users:
        client.post('/api/users/register', json=user_data)


def get_token_headers(client: TestClient, user_data: dict) -> dict:
    response = client.post('/api/auth/token', json=user_data)
    token = response.json()['access_token']
    return {"Authorization": f"Bearer {token}"}


if __name__ == "__main__":
    pass
