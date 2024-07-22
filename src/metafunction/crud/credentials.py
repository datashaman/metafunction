from typing import List, Optional

from metafunction.database import (
    Credential,
    CredentialCreate,
    CredentialUpdate,
    Session,
    select,
)


def get_all(session: Session, offset: int = 0, limit: int = 10) -> List[Credential]:
    return list(session.query(Credential).offset(offset).limit(limit).all())


def get(session: Session, credential_id: int) -> Optional[Credential]:
    return session.exec(select(Credential).where(Credential.id == credential_id)).first()


def get_by_name(session: Session, name: str) -> Optional[Credential]:
    return session.exec(select(Credential).where(Credential.name == name)).first()


def create(session: Session, data: CredentialCreate) -> Credential:
    credential = Credential.model_validate(data)
    session.add(credential)
    session.commit()
    session.refresh(credential)
    return credential


def update(session: Session, credential: Credential, data: CredentialUpdate) -> Credential:
    for key, value in data.model_dump().items():
        setattr(credential, key, value)
    session.commit()
    session.refresh(credential)
    return credential


def update_by_id(session: Session, credential_id: int, data: CredentialUpdate) -> Optional[Credential]:
    if credential := get(session, credential_id):
        return update(session, credential, data)
    return None


def delete(session: Session, credential: Credential) -> Credential:
    session.delete(credential)
    session.commit()
    return credential


def delete_by_id(session: Session, credential_id: int) -> Optional[Credential]:
    if credential := get(session, credential_id):
        return delete(session, credential)
    return None
