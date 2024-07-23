from typing import List, Optional

from metafunction.credentials.models import Credential, CredentialCreate, CredentialUpdate
from metafunction.database import (
    Session,
    select,
)
from metafunction.users.models import User


def get_all(
    session: Session,
    user: User,
    offset: int = 0,
    limit: int = 10,
) -> List[Credential]:
    return list(session.exec(select(Credential).where(Credential.user_id == user.id).offset(offset).limit(limit)).all())


def get(
    session: Session,
    user: User,
    credential_id: int,
) -> Optional[Credential]:
    return session.exec(
        select(Credential).where(Credential.user_id == user.id).where(Credential.id == credential_id)
    ).first()


def get_by_name(
    session: Session,
    user: User,
    name: str,
) -> Optional[Credential]:
    return session.exec(select(Credential).where(Credential.user_id == user.id).where(Credential.name == name)).first()


def create(
    session: Session,
    user: User,
    data: CredentialCreate,
) -> Credential:
    dump = data.model_dump()
    dump['user_id'] = user.id
    credential = Credential.model_validate(dump)
    session.add(credential)
    session.commit()
    session.refresh(credential)
    return credential


def update(
    session: Session,
    user: User,
    credential: Credential,
    data: CredentialUpdate,
) -> Credential:
    if credential.user_id != user.id:
        msg = 'Credential does not belong to user'
        raise ValueError(msg)

    for key, value in data.model_dump().items():
        setattr(credential, key, value)
    session.commit()
    session.refresh(credential)
    return credential


def update_by_id(session: Session, user: User, credential_id: int, data: CredentialUpdate) -> Optional[Credential]:
    if credential := get(session, user, credential_id):
        return update(session, user, credential, data)
    return None


def delete(session: Session, user: User, credential: Credential) -> Credential:
    if credential.user_id != user.id:
        msg = 'Credential does not belong to user'
        raise ValueError(msg)

    session.delete(credential)
    session.commit()
    return credential


def delete_by_id(session: Session, user: User, credential_id: int) -> Optional[Credential]:
    if credential := get(session, user, credential_id):
        return delete(session, user, credential)
    return None
