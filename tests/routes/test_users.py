from fastapi import status
from fastapi.testclient import TestClient

from metafunction.database import Session
from metafunction.repositories import users
from metafunction.users.models import User


def test_get_user(client: TestClient, admin_user: User) -> None:
    token = admin_user.create_access_token()

    response = client.get(
        f'/users/{admin_user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == status.HTTP_200_OK

    body = response.json()
    assert body['status'] == 'success'
    assert body['data']['user']['id'] == admin_user.id
    assert body['data']['user']['email'] == admin_user.email
    assert body['data']['user']['is_admin']

    assert 'password' not in body['data']['user']


def test_get_user_invalid(client: TestClient, admin_user: User) -> None:
    token = admin_user.create_access_token()

    response = client.get(
        '/users/999',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND

    body = response.json()
    assert body['status'] == 'fail'
    assert body['data']['user_id'] == 'User not found'


def test_get_users(client: TestClient, admin_user: User) -> None:
    token = admin_user.create_access_token()

    response = client.get(
        '/users',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == status.HTTP_200_OK

    body = response.json()
    assert body['status'] == 'success'
    assert len(body['data']['users']) == 1

    user = body['data']['users'][0]
    assert user['id'] == admin_user.id
    assert user['email'] == admin_user.email
    assert user['is_admin']

    assert 'password' not in user


def test_create_user(client: TestClient, session: Session, admin_user: User) -> None:
    token = admin_user.create_access_token()

    json = {
        'email': 'test1@example.com',
        'name': 'Test User 1',
        'password': 'password',
    }

    response = client.post(
        '/users',
        headers={'Authorization': f'Bearer {token}'},
        json=json,
    )

    assert response.status_code == status.HTTP_201_CREATED

    body = response.json()
    assert body['status'] == 'success'

    user = body['data']['user']
    assert user['email'] == json['email']
    assert user['name'] == json['name']
    assert not user['is_admin']

    assert 'password' not in body['data']['user']

    db_user = users.get(session, None, user['id'])
    assert db_user is not None
    assert db_user.email == json['email']
    assert db_user.name == json['name']
    assert not db_user.is_admin


def test_create_user_invalid_email(client: TestClient, test_user: User, admin_user: User) -> None:
    token = admin_user.create_access_token()

    json = {
        'email': test_user.email,
        'name': 'Test User 1',
        'password': 'password',
    }

    response = client.post(
        '/users',
        headers={'Authorization': f'Bearer {token}'},
        json=json,
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    body = response.json()
    assert body['status'] == 'fail'
    assert body['data'] == {'email': 'User email exists'}


def test_create_user_invalid_name(client: TestClient, test_user: User, admin_user: User) -> None:
    token = admin_user.create_access_token()

    json = {
        'email': 'test1@example.com',
        'name': test_user.name,
        'password': 'password',
    }

    response = client.post(
        '/users',
        headers={'Authorization': f'Bearer {token}'},
        json=json,
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    body = response.json()
    assert body['status'] == 'fail'
    assert body['data'] == {'name': 'User name exists'}


def test_update_user(client: TestClient, session: Session, test_user: User, admin_user: User) -> None:
    token = admin_user.create_access_token()

    json = {
        'email': 'test1@example.com',
        'name': 'Test User 1',
    }

    response = client.put(
        f'/users/{test_user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json=json,
    )

    assert response.status_code == status.HTTP_200_OK

    body = response.json()
    assert body['status'] == 'success'

    user = body['data']['user']
    assert user['email'] == json['email']
    assert user['name'] == json['name']

    assert 'password' not in user

    assert test_user.id is not None
    db_user = users.get(session, None, test_user.id)
    assert db_user is not None
    assert db_user.email == json['email']
    assert db_user.name == json['name']


def test_update_user_invalid(client: TestClient, test_user: User, admin_user: User) -> None:
    token = admin_user.create_access_token()

    response = client.put(
        '/users/999',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'email': 'test2@example.com',
            'name': 'Test User 2',
        },
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND

    body = response.json()
    assert body['status'] == 'fail'
    assert body['data']['user_id'] == 'User not found'


def test_update_user_invalid_email(client: TestClient, test_user: User, admin_user: User) -> None:
    token = admin_user.create_access_token()

    json = {
        'email': admin_user.email,
        'name': test_user.name,
    }

    response = client.put(
        f'/users/{test_user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json=json,
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    body = response.json()
    assert body['status'] == 'fail'
    assert body['data'] == {'email': 'User email exists'}


def test_update_user_invalid_name(client: TestClient, test_user: User, admin_user: User) -> None:
    token = admin_user.create_access_token()

    json = {
        'email': test_user.email,
        'name': admin_user.name,
        'password': 'password',
    }

    response = client.put(
        f'/users/{test_user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json=json,
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    body = response.json()
    assert body['status'] == 'fail'
    assert body['data'] == {'name': 'User name exists'}


def test_delete_user(client: TestClient, session: Session, test_user: User, admin_user: User) -> None:
    token = admin_user.create_access_token()

    response = client.delete(
        f'/users/{test_user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == status.HTTP_200_OK

    body = response.json()
    assert body['status'] == 'success'
    assert body['data']['user']['id'] == test_user.id
    assert body['data']['user']['email'] == test_user.email
    assert not body['data']['user']['is_admin']

    assert 'password' not in body['data']['user']

    db_user = users.get(session, None, test_user.id)
    assert db_user is None


def test_delete_user_invalid(client: TestClient, test_user: User, admin_user: User) -> None:
    token = admin_user.create_access_token()

    response = client.delete(
        '/users/999',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND

    body = response.json()
    assert body['status'] == 'fail'
    assert body['data']['user_id'] == 'User not found'


def test_nonadmin_user(client: TestClient, test_user: User) -> None:
    token = test_user.create_access_token()

    response = client.get(
        f'/users/{test_user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN

    body = response.json()
    assert body['status'] == 'error'
    assert body['message'] == 'You are not an admin'
