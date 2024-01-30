from pathlib import Path

from fastapi.testclient import TestClient

from src.config import settings
from tests.app.files.test_upload import TEST_FILE_DIR


def test_download_file(client: TestClient, user1_token_headers):
    with open(Path(TEST_FILE_DIR, 'favicon_1.png'), 'rb') as f:
        response_upload = client.post(
            '/api/files/upload',
            files={'file': f},
            headers=user1_token_headers
        )
    assert response_upload.status_code == 200
    response_download = client.get(
        '/api/files/download/1',
        headers=user1_token_headers
    )
    assert response_download.status_code == 200
