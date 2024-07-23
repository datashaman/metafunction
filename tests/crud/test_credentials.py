from metafunction.credentials import crud as credentials
from metafunction.credentials.models import (
    Credential,
    CredentialCreate,
    CredentialType,
    CredentialTypeCreate,
    CredentialUpdate,
)
from metafunction.database import Session
from metafunction.users.models import User


def test_get_all(session: Session, test_user: User):
    credentials_list = credentials.get_all(session, test_user)
    assert len(credentials_list) == 0


def test_get_all_with_rows(session: Session, test_user: User, test_credential: Credential):
    credentials_list = credentials.get_all(session, test_user)
    assert len(credentials_list) == 1
    assert credentials_list[0].id == test_credential.id


def test_get(session: Session, test_user: User, test_credential: Credential):
    assert test_credential.id is not None
    credential = credentials.get(session, test_user, test_credential.id)
    assert credential is not None
    assert credential.id == test_credential.id


def test_get_by_name(session: Session, test_user: User, test_credential: Credential):
    credential = credentials.get_by_name(session, test_user, test_credential.name)
    assert credential is not None
    assert credential.id == test_credential.id


def test_get_not_found(session: Session, test_user: User):
    credential = credentials.get(session, test_user, 1)
    assert credential is None


def test_create(session: Session, test_user: User):
    credential_type = CredentialType.model_validate(CredentialTypeCreate(id='password', name='Password'))

    session.add(credential_type)
    session.commit()
    session.refresh(credential_type)

    credential = credentials.create(
        session,
        test_user,
        CredentialCreate.model_validate(
            {
                'name': 'Test Credential 1',
                'credential_type_id': credential_type.id,
                'data': {},
            }
        ),
    )
    assert credential.id is not None


def test_update(session: Session, test_user: User, test_credential: Credential):
    credential = credentials.update(
        session,
        test_user,
        test_credential,
        CredentialUpdate.model_validate(
            {
                'name': 'Test Credential 2',
                'credential_type_id': test_credential.credential_type_id,
                'data': test_credential.data,
            }
        ),
    )
    assert credential.name == 'Test Credential 2'


def test_update_by_id(session: Session, test_user: User, test_credential: Credential):
    assert test_credential.id is not None
    credential = credentials.update_by_id(
        session,
        test_user,
        test_credential.id,
        CredentialUpdate.model_validate(
            {
                'name': 'Test Credential 2',
                'credential_type_id': test_credential.credential_type_id,
                'data': test_credential.data,
            }
        ),
    )
    assert credential is not None
    assert credential.name == 'Test Credential 2'


def test_update_by_unknown_id(session: Session, test_user: User):
    credential = credentials.update_by_id(
        session,
        test_user,
        1,
        CredentialUpdate.model_validate(
            {
                'name': 'Test Credential 2',
                'credential_type_id': 'password',
                'data': {},
            }
        ),
    )
    assert credential is None


def test_delete(session: Session, test_user: User, test_credential: Credential):
    credential = credentials.delete(session, test_user, test_credential)
    assert test_credential.id is not None
    assert credential is not None
    assert credential.id == test_credential.id
    assert credentials.get(session, test_user, test_credential.id) is None


def test_delete_by_id(session: Session, test_user: User, test_credential: Credential):
    assert test_credential.id is not None
    credential = credentials.delete_by_id(session, test_user, test_credential.id)
    assert credential is not None
    assert credential.id == test_credential.id
    assert credentials.get(session, test_user, test_credential.id) is None


def test_delete_by_unknown_id(session: Session, test_user: User):
    credential = credentials.delete_by_id(session, test_user, 1)
    assert credential is None
