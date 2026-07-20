from fastapi import APIRouter
from starlette import status
from backend.dependencies.recipe import RecipeServiceDep
from backend.schemas.recipes import RecipeCreate, RecipeUpdate

router = APIRouter(
    prefix="/recipes",
    tags=["recipes"],
)


@router.get("/", status_code=status.HTTP_200_OK, summary="Список рецептов")
async def get_all_recipes(service: RecipeServiceDep):
    return await service.get_all()


@router.get(
    "/{recipe_id}",
    status_code=status.HTTP_200_OK,
    summary="Один рецепт"
)
async def get_recipe(
        recipe_id: int,
        service: RecipeServiceDep
):
    return await service.get_or_404(recipe_id)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Создать рецепт"
)
async def create_recipe(
        recipe_in: RecipeCreate,
        service: RecipeServiceDep
):
    return await service.create(recipe_in)


@router.patch(
    "/{recipe_id}",
    status_code=status.HTTP_200_OK,
    summary="Обновить рецепт"
)
async def update_recipe(
        recipe_id: int,
        body: RecipeUpdate,
        service: RecipeServiceDep
):
    return await service.update(recipe_id, body)


@router.delete(
    "/{recipe_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить рецепт"
)
async def delete_recipe(
        recipe_id: int,
        service: RecipeServiceDep
):
    return await service.delete(recipe_id)
