import pytest  # type: ignore
from fastapi.testclient import TestClient

from metafunction import app


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)
