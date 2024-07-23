from fastapi import status
from fastapi.testclient import TestClient

from metafunction.crud import functions
from metafunction.database import Function, Session, User


def test_get_function(client: TestClient, test_user: User, test_function: Function) -> None:
    token = test_user.create_access_token()

    response = client.get(
        f'/functions/{test_function.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == status.HTTP_200_OK

    body = response.json()
    assert body['status'] == 'success'
    assert body['data']['function']['id'] == test_function.id
    assert body['data']['function']['name'] == test_function.name
    assert body['data']['function']['specification'] == test_function.specification


def test_get_function_not_found(client: TestClient, test_user: User) -> None:
    token = test_user.create_access_token()

    response = client.get(
        '/functions/999',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND

    body = response.json()
    assert body['status'] == 'fail'
    assert body['data']['function_id'] == 'Function not found'


def test_get_functions(client: TestClient, test_user: User, test_function: Function) -> None:
    token = test_user.create_access_token()

    response = client.get(
        '/functions',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == status.HTTP_200_OK

    body = response.json()
    assert body['status'] == 'success'
    assert len(body['data']['functions']) == 1

    function = body['data']['functions'][0]
    assert function['id'] == test_function.id
    assert function['name'] == test_function.name
    assert function['specification'] == test_function.specification


def test_create_function(client: TestClient, session: Session, test_user: User) -> None:
    token = test_user.create_access_token()

    json = {
        'name': 'Test function 1',
        'specification': {'key': 'value'},
    }

    response = client.post(
        '/functions',
        headers={'Authorization': f'Bearer {token}'},
        json=json,
    )

    assert response.status_code == status.HTTP_201_CREATED

    body = response.json()
    assert body['status'] == 'success'
    assert body['data']['function']['name'] == json['name']
    assert body['data']['function']['specification'] == json['specification']

    function = functions.get(session, body['data']['function']['id'])
    assert function is not None
    assert function.name == json['name']
    assert function.specification == json['specification']


def test_update_function(client: TestClient, session: Session, test_user: User, test_function: Function) -> None:
    token = test_user.create_access_token()

    json = {
        'name': 'Test function 2',
        'specification': {'key': 'value2'},
    }

    response = client.put(
        f'/functions/{test_function.id}',
        headers={'Authorization': f'Bearer {token}'},
        json=json,
    )

    assert response.status_code == status.HTTP_200_OK

    body = response.json()
    assert body['status'] == 'success'
    assert body['data']['function']['name'] == json['name']
    assert body['data']['function']['specification'] == json['specification']

    assert test_function.id is not None
    function = functions.get(session, test_function.id)
    assert function is not None
    assert function.name == json['name']
    assert function.specification == json['specification']


def test_update_function_not_found(client: TestClient, test_user: User) -> None:
    token = test_user.create_access_token()

    json = {
        'name': 'Test function 2',
        'specification': {'key': 'value2'},
    }

    response = client.put(
        '/functions/999',
        headers={'Authorization': f'Bearer {token}'},
        json=json,
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND

    body = response.json()
    assert body['status'] == 'fail'
    assert body['data']['function_id'] == 'Function not found'


def test_delete_function(client: TestClient, session: Session, test_user: User, test_function: Function) -> None:
    token = test_user.create_access_token()

    response = client.delete(
        f'/functions/{test_function.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == status.HTTP_200_OK

    assert test_function.id is not None
    function = functions.get(session, test_function.id)
    assert function is None


def test_delete_function_not_found(client: TestClient, test_user: User) -> None:
    token = test_user.create_access_token()

    response = client.delete(
        '/functions/999',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND

    body = response.json()
    assert body['status'] == 'fail'
    assert body['data']['function_id'] == 'Function not found'
