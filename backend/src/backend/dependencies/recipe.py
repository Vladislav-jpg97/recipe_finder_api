from typing import Annotated

from fastapi import Depends

from backend.dependencies.database import SessionDep
from backend.repository.recipe_repo import RecipeRepository
from backend.repository.ingredient_repo import IngredientRepository
from backend.services.recipe_service import RecipeService


async def get_recipe_repo(
        session: SessionDep,
) -> RecipeRepository:
    return RecipeRepository(session)


RecipeRepoDep = Annotated[RecipeRepository, Depends(get_recipe_repo)]


async def get_ingredient_repo(
        session: SessionDep,
) -> IngredientRepository:
    return IngredientRepository(session)


IngredientRepoDep = Annotated[IngredientRepository, Depends(get_ingredient_repo)]


async def get_recipe_service(
        session: SessionDep,
        recipe_repo: RecipeRepoDep,
        ingredient_repo: IngredientRepoDep,  # <-- Добавили зависимость репозитория ингредиентов
) -> RecipeService:
    return RecipeService(
        session=session,
        recipe_repo=recipe_repo,
        ingredient_repo=ingredient_repo,  # <-- Передали его в сервис
    )


RecipeServiceDep = Annotated[RecipeService, Depends(get_recipe_service)]