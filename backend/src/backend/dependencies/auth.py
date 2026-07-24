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

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


async def get_current_user(
        user_repo: UserRepoDep,
        token: str = Depends(oauth2_scheme),

):
    user_id = decode_token(token, expected_type="access")

    user = await user_repo.get_by_id(user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )
    return user
