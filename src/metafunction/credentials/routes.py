from typing import List, Union

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from metafunction.auth import get_current_user
from metafunction.credentials.models import CredentialCreate, CredentialPublic
from metafunction.database import Session, get_session
from metafunction.repositories import credentials
from metafunction.responses import FailResponse, SuccessResponse, fail_response, success_response
from metafunction.users.models import User

router = APIRouter()


@router.get(
    '/',
    response_model=SuccessResponse[List[CredentialPublic]],
)
async def list_credentials(
    offset: int = 0,
    limit: int = 10,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> JSONResponse:
    return success_response(
        credentials=[
            CredentialPublic.model_validate(credential)
            for credential in credentials.get_all(session, current_user, offset=offset, limit=limit)
        ]
    )


@router.get(
    '/{credential_id}',
    response_model=Union[SuccessResponse[CredentialPublic], FailResponse],
)
async def read_credential(
    credential_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> JSONResponse:
    if credential := credentials.get(session, current_user, credential_id):
        return success_response(credential=CredentialPublic.model_validate(credential))
    return fail_response(status_code=404, credential_id='Credential not found')


@router.post(
    '/',
    response_model=SuccessResponse[CredentialPublic],
)
async def create_credential(
    data: CredentialCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> JSONResponse:
    credential = credentials.create(session, current_user, data)
    return success_response(status_code=201, credential=CredentialPublic.model_validate(credential))


@router.delete(
    '/{credential_id}',
    response_model=Union[SuccessResponse[CredentialPublic], FailResponse],
)
async def delete_credential(
    credential_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> JSONResponse:
    if credential := credentials.delete_by_id(session, current_user, credential_id):
        return success_response(credential=CredentialPublic.model_validate(credential))
    return fail_response(status_code=404, credential_id='Credential not found')
