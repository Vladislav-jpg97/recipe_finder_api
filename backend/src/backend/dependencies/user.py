from typing import Annotated

from fastapi import Depends
from backend.dependencies.database import SessionDep
from backend.repository.user_repo import UserRepository
async def get_auth_repo(
        session: SessionDep
):
    return UserRepository(session)


UserRepoDep = Annotated[
    UserRepository,
    Depends(get_auth_repo)
]