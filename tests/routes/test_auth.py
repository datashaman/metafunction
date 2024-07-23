from fastapi import status
from fastapi.testclient import TestClient

from metafunction.database import Session
from metafunction.users.models import User


def test_login(client: TestClient, test_user: User, session: Session) -> None:
    response = client.post(
        '/auth/token',
        data={
            'username': test_user.email,
            'password': test_user.password,
        },
    )

    assert response.status_code == status.HTTP_200_OK

    body = response.json()
    assert body['access_token'] is not None


def test_login_invalid_username(client: TestClient, test_user: User) -> None:
    response = client.post(
        '/auth/token',
        data={
            'username': 'invalid',
            'password': test_user.password,
        },
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    body = response.json()
    assert body['status'] == 'fail'
    assert body['data']['username'] == 'Incorrect username or password'


def test_login_invalid_password(client: TestClient, test_user: User) -> None:
    response = client.post(
        '/auth/token',
        data={
            'username': test_user.email,
            'password': 'invalid',
        },
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    body = response.json()
    assert body['status'] == 'fail'
    assert body['data']['username'] == 'Incorrect username or password'


def test_unauthorized_me(client: TestClient) -> None:
    response = client.get('/auth/me')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    body = response.json()
    assert body['status'] == 'error'
    assert body['message'] == 'Not authenticated'


def test_authorized_me(client: TestClient, test_user: User) -> None:
    token = test_user.create_access_token()

    response = client.get(
        '/auth/me',
        headers={
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
        },
    )

    assert response.status_code == status.HTTP_200_OK

    body = response.json()

    assert body['data']['user']['email'] == test_user.email
    assert body['data']['user']['name'] == test_user.name
    assert 'password' not in body['data']['user']
