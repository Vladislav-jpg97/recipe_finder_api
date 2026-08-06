from typing import Annotated

from fastapi import Depends

from backend.dependencies.database import SessionDep
from backend.repository.cuisine_repo import CuisineRepository
from backend.services.cuisine_service import CuisineService


async def get_cuisine_repo(
        session: SessionDep
) -> CuisineRepository:
    return CuisineRepository(session)

CuisineRepoDep = Annotated[
    CuisineRepository, Depends(get_cuisine_repo)
]

async def get_cuisine_service(
        session: SessionDep,
        cuisine_repo: CuisineRepoDep,
) -> CuisineService:
    return CuisineService(
        session=session,
        cuisine_repo=cuisine_repo
    )

CuisineServiceDep = Annotated[
    CuisineService, Depends(get_cuisine_service)
]