from typing import Annotated

from fastapi import Depends
from backend.dependencies.database import SessionDep
from backend.dependencies.user import UserRepoDep
from backend.services.user_service import UserService
from backend.core.cache import cache


async def get_user_service(
        session: SessionDep,
        user_repo: UserRepoDep
):
    return UserService(session=session, user_repo=user_repo, cache_service=cache)


UserServiceDep = Annotated[
    UserService,
    Depends(get_user_service)
]