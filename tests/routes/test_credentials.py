from fastapi import status
from fastapi.testclient import TestClient

from metafunction.credentials.models import Credential
from metafunction.database import Session
from metafunction.repositories import credentials
from metafunction.users.models import User


def test_get_credential(client: TestClient, test_user: User, test_credential: Credential) -> None:
    token = test_user.create_access_token()

    response = client.get(
        f'/credentials/{test_credential.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == status.HTTP_200_OK

    body = response.json()
    assert body['status'] == 'success'
    assert body['data']['credential']['id'] == test_credential.id
    assert body['data']['credential']['name'] == test_credential.name
    assert body['data']['credential']['data'] == test_credential.data


def test_get_credential_not_found(client: TestClient, test_user: User) -> None:
    token = test_user.create_access_token()

    response = client.get(
        '/credentials/999',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND

    body = response.json()
    assert body['status'] == 'fail'
    assert body['data']['credential_id'] == 'Credential not found'


def test_get_credentials(client: TestClient, test_user: User, test_credential: Credential) -> None:
    token = test_user.create_access_token()

    response = client.get(
        '/credentials',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == status.HTTP_200_OK

    body = response.json()
    assert body['status'] == 'success'
    assert len(body['data']['credentials']) == 1

    credential = body['data']['credentials'][0]
    assert credential['id'] == test_credential.id
    assert credential['name'] == test_credential.name
    assert credential['data'] == test_credential.data


def test_create_credential(client: TestClient, session: Session, test_user: User) -> None:
    token = test_user.create_access_token()

    json = {
        'name': 'Test Credential 1',
        'credential_type_id': 'password',
        'data': {'key': 'value'},
    }

    response = client.post(
        '/credentials',
        headers={'Authorization': f'Bearer {token}'},
        json=json,
    )

    assert response.status_code == status.HTTP_201_CREATED

    body = response.json()
    assert body['status'] == 'success'
    assert body['data']['credential']['name'] == json['name']
    assert body['data']['credential']['data'] == json['data']

    credential = credentials.get(session, test_user, body['data']['credential']['id'])
    assert credential is not None
    assert credential.name == json['name']
    assert credential.data == json['data']
    assert credential.user_id == test_user.id


def test_delete_credential(client: TestClient, session: Session, test_user: User, test_credential: Credential) -> None:
    token = test_user.create_access_token()

    response = client.delete(
        f'/credentials/{test_credential.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == status.HTTP_200_OK

    body = response.json()
    assert body['status'] == 'success'

    assert test_credential.id is not None
    credential = credentials.get(session, test_user, test_credential.id)
    assert credential is None


def test_delete_credential_not_found(client: TestClient, test_user: User) -> None:
    token = test_user.create_access_token()

    response = client.delete(
        '/credentials/999',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND

    body = response.json()
    assert body['status'] == 'fail'
    assert body['data']['credential_id'] == 'Credential not found'
