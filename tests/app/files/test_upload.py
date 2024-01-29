from pathlib import Path

from fastapi.testclient import TestClient

from src.config import settings

TEST_FILE_DIR = Path(settings.BASE_DIR, 'tests', 'app', 'files', 'files_for_test')


def test_upload_file(client: TestClient, user1_token_headers):
    with open(Path(TEST_FILE_DIR, 'favicon_1.png'), 'rb') as f:
        response = client.post(
            '/api/files/upload',
            files={'file': f},
            headers=user1_token_headers)
    assert response.status_code == 200
    assert response.json() == {'file': 'favicon_1.png'}


def test_upload_multiple_file(client: TestClient, user1_token_headers):
    with open(Path(TEST_FILE_DIR, 'favicon_1.png'), 'rb') as f:
        response = client.post(
            '/api/files/upload/multiple',
            files={'files': f},
            headers=user1_token_headers)
    assert response.status_code == 200
    assert response.json() == {'files': ['favicon_1.png'], 'total': 1}


def test_upload_public_file(client: TestClient, admin_token_headers):
    with open(Path(TEST_FILE_DIR, 'favicon_1.png'), 'rb') as f:
        response = client.post(
            '/api/files/upload/public',
            files={'file': f},
            headers=admin_token_headers)
    assert response.status_code == 200
    assert response.json() == {'file': 'favicon_1.png'}


def test_upload_public_file_error403(client: TestClient, user1_token_headers):
    with open(Path(TEST_FILE_DIR, 'favicon_1.png'), 'rb') as f:
        response = client.post(
            '/api/files/upload/public',
            files={'file': f},
            headers=user1_token_headers)
    assert response.status_code == 403
    assert response.json() == {'detail': "The user doesn't have enough privileges"}


def test_upload_multiple_public_file(client: TestClient, admin_token_headers):
    with open(Path(TEST_FILE_DIR, 'favicon_1.png'), 'rb') as f:
        response = client.post(
            '/api/files/upload/public/multiple',
            files={'files': f},
            headers=admin_token_headers)
    assert response.status_code == 200
    assert response.json() == {'files': ['favicon_1.png'], 'total': 1}


def test_upload_multiple_public_file_error403(client: TestClient, user1_token_headers):
    with open(Path(TEST_FILE_DIR, 'favicon_1.png'), 'rb') as f:
        response = client.post(
            '/api/files/upload/public/multiple',
            files={'files': f},
            headers=user1_token_headers)
    assert response.status_code == 403
    assert response.json() == {'detail': "The user doesn't have enough privileges"}
