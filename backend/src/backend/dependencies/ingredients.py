from typing import Annotated

from fastapi import Depends

from backend.dependencies.database import SessionDep
from backend.repository.ingredient_repo import IngredientRepository
from backend.services.ingredient_service import IngredientService


async def get_ingredient_repo(session: SessionDep) -> IngredientRepository:
    return IngredientRepository(session)


IngredientRepoDep = Annotated[
    IngredientRepository, Depends(get_ingredient_repo)
]


async def get_ingredient_service(
        session: SessionDep,
        ingredient_repo: IngredientRepoDep
) -> IngredientService:
    return IngredientService(
        session=session,
        ingredient_repo=ingredient_repo
    )


IngredientServiceDep = Annotated[
    IngredientService, Depends(get_ingredient_service)
]