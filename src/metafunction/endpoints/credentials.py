from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from typing import List, Sequence, Union

from metafunction.database import (
    get_session,
    Session,
    select,
    Credential,
    CredentialCreate,
    CredentialPublic,
)
from metafunction.helpers import success_response, fail_response
from metafunction.responses import SuccessResponse, FailResponse


router = APIRouter()


@router.get("/", response_model=SuccessResponse[List[CredentialPublic]])
async def list_credentials(
    offset: int = 0, limit: int = 10, session: Session = Depends(get_session)
) -> JSONResponse:
    statement = select(Credential).offset(offset).limit(limit)
    return success_response(
        data=[
            CredentialPublic.model_validate(credential)
            for credential in session.exec(statement)
        ]
    )


@router.get(
    "/{credential_id}",
    response_model=Union[SuccessResponse[CredentialPublic], FailResponse],
)
async def read_credential(
    credential_id: int, session: Session = Depends(get_session)
) -> JSONResponse:
    credential = session.get(Credential, credential_id)
    if credential is None:
        return fail_response(
            data={"credential_id": "Credential not found"}, status_code=404
        )
    return success_response(data=CredentialPublic.model_validate(credential))


@router.post("/", response_model=SuccessResponse[CredentialPublic])
async def create_credential(
    data: CredentialCreate, session: Session = Depends(get_session)
) -> JSONResponse:
    credential = Credential.model_validate(data.dict())
    session.add(credential)
    session.commit()
    session.refresh(credential)
    return success_response(data=CredentialPublic.model_validate(credential))


@router.delete(
    "/{credential_id}",
    response_model=Union[SuccessResponse[CredentialPublic], FailResponse],
)
async def delete_credential(
    credential_id: int, session: Session = Depends(get_session)
) -> JSONResponse:
    credential = session.get(Credential, credential_id)
    if credential is None:
        return fail_response(
            data={"credential_id": "Credential not found"}, status_code=404
        )
    session.delete(credential)
    session.commit()
    return success_response(data=CredentialPublic.model_validate(credential))
