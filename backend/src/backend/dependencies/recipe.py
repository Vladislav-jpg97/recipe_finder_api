from typing import Annotated

from fastapi import Depends

from backend.dependencies.database import SessionDep
from backend.repository.recipe_repo import RecipeRepository
from backend.services.recipe_service import RecipeService


async def get_recipe_repo(
        session: SessionDep,
) -> RecipeRepository:
    return RecipeRepository(session)


RecipeRepoDep = Annotated[RecipeRepository, Depends(get_recipe_repo)]


async def get_recipe_service(
        session: SessionDep,
        recipe_repo: RecipeRepoDep,
) -> RecipeService:
    return RecipeService(
        session=session,
        recipe_repo=recipe_repo
    )


RecipeServiceDep = Annotated[RecipeService, Depends(get_recipe_service)]
