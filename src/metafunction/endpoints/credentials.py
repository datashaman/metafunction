from typing import List, Union

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from metafunction.auth import get_current_user
from metafunction.crud import credentials
from metafunction.database import (
    CredentialCreate,
    CredentialPublic,
    Session,
    get_session,
)
from metafunction.helpers import fail_response, success_response
from metafunction.responses import FailResponse, SuccessResponse

router = APIRouter()


@router.get(
    '/',
    response_model=SuccessResponse[List[CredentialPublic]],
    dependencies=[Depends(get_current_user)],
)
async def list_credentials(offset: int = 0, limit: int = 10, session: Session = Depends(get_session)) -> JSONResponse:
    return success_response(
        credentials=[
            CredentialPublic.model_validate(credential)
            for credential in credentials.get_all(session, offset=offset, limit=limit)
        ]
    )


@router.get(
    '/{credential_id}',
    response_model=Union[SuccessResponse[CredentialPublic], FailResponse],
    dependencies=[Depends(get_current_user)],
)
async def read_credential(credential_id: int, session: Session = Depends(get_session)) -> JSONResponse:
    if credential := credentials.get(session, credential_id):
        return success_response(credential=CredentialPublic.model_validate(credential))
    return fail_response(status_code=404, credential_id='Credential not found')


@router.post(
    '/',
    response_model=SuccessResponse[CredentialPublic],
    dependencies=[Depends(get_current_user)],
)
async def create_credential(data: CredentialCreate, session: Session = Depends(get_session)) -> JSONResponse:
    credential = credentials.create(session, data)
    return success_response(status_code=201, credential=CredentialPublic.model_validate(credential))


@router.delete(
    '/{credential_id}',
    response_model=Union[SuccessResponse[CredentialPublic], FailResponse],
    dependencies=[Depends(get_current_user)],
)
async def delete_credential(credential_id: int, session: Session = Depends(get_session)) -> JSONResponse:
    if credential := credentials.delete_by_id(session, credential_id):
        return success_response(credential=CredentialPublic.model_validate(credential))
    return fail_response(status_code=404, credential_id='Credential not found')
