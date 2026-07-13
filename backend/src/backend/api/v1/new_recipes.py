from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from backend.core.database import get_db
from backend.repository.recipe_repo import RecipeRepository
from backend.schemas.recipes import RecipeCreate, RecipeUpdate
from backend.services.recipe_service import RecipeService

router = APIRouter(
    prefix="/recipes",
    tags=["recipes"],
)


@router.get("/", status_code=status.HTTP_200_OK, summary="Список рецептов")
async def get_all_recipes(session: AsyncSession = Depends(get_db)):
    repo = RecipeRepository(session)
    service = RecipeService(repo, session)
    return await service.get_all()


@router.get(
    "/{recipe_id}",
    status_code=status.HTTP_200_OK,
    summary="Один рецепт"
)
async def get_recipe(
        recipe_id: int,
        session: AsyncSession = Depends(get_db)
):
    repo = RecipeRepository(session)
    service = RecipeService(repo, session)
    return await service.get_or_404(recipe_id)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Создать рецепт"
)
async def create_recipe(
        recipe_in: RecipeCreate,
        session: AsyncSession = Depends(get_db)
):
    repo = RecipeRepository(session)
    service = RecipeService(repo, session)
    return await service.create(recipe_in)


@router.patch(
    "/{recipe_id}",
    status_code=status.HTTP_200_OK,
    summary="Обновить рецепт"
)
async def update_recipe(
        recipe_id: int,
        body: RecipeUpdate,
        session: AsyncSession = Depends(get_db)
):
    repo = RecipeRepository(session)
    service = RecipeService(repo, session)
    return await service.update(recipe_id, body)


@router.delete(
    "/{recipe_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить рецепт"
)
async def delete_recipe(
        recipe_id: int,
        session: AsyncSession = Depends(get_db)
):
    repo = RecipeRepository(session)
    service = RecipeService(repo, session)
    return await service.delete(recipe_id)
