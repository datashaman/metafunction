from fastapi import APIRouter, Depends, HTTPException
from typing import List, Sequence

from metafunction.models import (
    get_session,
    Session,
    select,
    Credential,
    CredentialCreate,
    CredentialPublic,
)


router = APIRouter()


@router.get("/", response_model=List[Credential])
async def list_credentials(
    offset: int = 0, limit: int = 10, session: Session = Depends(get_session)
) -> List[CredentialPublic]:
    statement = select(Credential).offset(offset).limit(limit)
    return [
        CredentialPublic.from_orm(credential) for credential in session.exec(statement)
    ]


@router.get("/{credential_id}", response_model=CredentialPublic)
async def read_credential(
    credential_id: int, session: Session = Depends(get_session)
) -> CredentialPublic:
    credential = session.get(Credential, credential_id)
    if credential is None:
        raise HTTPException(status_code=404, detail="Credential not found")
    return CredentialPublic.from_orm(credential)


@router.post("/", response_model=Credential)
async def create_credential(
    data: CredentialCreate, session: Session = Depends(get_session)
) -> CredentialPublic:
    credential = Credential(**data.dict())
    session.add(credential)
    session.commit()
    session.refresh(credential)
    return CredentialPublic.from_orm(credential)


@router.delete("/{credential_id}", response_model=CredentialPublic)
async def delete_credential(
    credential_id: int, session: Session = Depends(get_session)
) -> CredentialPublic:
    credential = session.get(Credential, credential_id)
    if credential is None:
        raise HTTPException(status_code=404, detail="Credential not found")
    session.delete(credential)
    session.commit()
    return CredentialPublic.from_orm(credential)
