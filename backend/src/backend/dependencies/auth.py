from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from starlette import status

from backend.core.security import decode_token
from backend.dependencies.database import SessionDep
from backend.repository.user_repo import UserRepository
from backend.services.user_service import UserService


async def get_auth_repo(
        session: SessionDep
):
    return UserRepository(session)


UserRepoDep = Annotated[
    UserRepository,
    Depends(get_auth_repo)
]


async def get_user_service(
        session: SessionDep,
        user_repo: UserRepoDep
):
    return UserService(session=session, user_repo=user_repo)


UserServiceDep = Annotated[
    UserService,
    Depends(get_user_service)
]





