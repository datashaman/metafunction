from typing import Dict, Any

from fastapi.testclient import TestClient

from metafunction import app
from metafunction.models import Session


def test_login(client: TestClient, test_user: Dict[str, Any], session: Session) -> None:
    response = client.post(
        "/auth/token",
        data={"username": test_user["email"], "password": test_user["password"]},
    )

    assert response.status_code == 200
    assert response.json()["access_token"] is not None
