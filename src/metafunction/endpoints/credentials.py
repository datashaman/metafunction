from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from typing import List, Sequence, Union

from metafunction.crud import credentials
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
from metafunction.security.oauth2 import get_current_user


router = APIRouter()


@router.get(
    "/",
    response_model=SuccessResponse[List[CredentialPublic]],
    dependencies=[Depends(get_current_user)],
)
async def list_credentials(
    offset: int = 0, limit: int = 10, session: Session = Depends(get_session)
) -> JSONResponse:
    return success_response(
        credentials=[
            CredentialPublic.model_validate(credential)
            for credential in credentials.list(session, offset=offset, limit=limit)
        ]
    )


@router.get(
    "/{credential_id}",
    response_model=Union[SuccessResponse[CredentialPublic], FailResponse],
    dependencies=[Depends(get_current_user)],
)
async def read_credential(
    credential_id: int, session: Session = Depends(get_session)
) -> JSONResponse:
    if credential := credentials.get(session, credential_id):
        return success_response(credential=CredentialPublic.model_validate(credential))
    return fail_response(
        data={"credential_id": "Credential not found"}, status_code=404
    )


@router.post(
    "/",
    response_model=SuccessResponse[CredentialPublic],
    dependencies=[Depends(get_current_user)],
)
async def create_credential(
    data: CredentialCreate, session: Session = Depends(get_session)
) -> JSONResponse:
    credential = credentials.create(session, data)
    return success_response(credential=CredentialPublic.model_validate(credential))


@router.delete(
    "/{credential_id}",
    response_model=Union[SuccessResponse[CredentialPublic], FailResponse],
    dependencies=[Depends(get_current_user)],
)
async def delete_credential(
    credential_id: int, session: Session = Depends(get_session)
) -> JSONResponse:
    if credential := credentials.delete_by_id(session, credential_id):
        return success_response(credential=CredentialPublic.model_validate(credential))
    return fail_response(
        data={"credential_id": "Credential not found"}, status_code=404
    )
