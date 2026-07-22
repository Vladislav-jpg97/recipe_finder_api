from fastapi import APIRouter, Depends, Query
from starlette import status
from backend.dependencies.recipe import RecipeServiceDep
from backend.schemas.pagination import Page, PaginationParams
from backend.schemas.recipes import RecipeCreate, RecipeUpdate, RecipeDetail, RecipeFilters
from backend.services.recipe_service import RecipeService

router = APIRouter(
    prefix="/recipes",
    tags=["recipes"],
)


@router.get("/", status_code=status.HTTP_200_OK, response_model=Page[RecipeDetail], summary="Список рецептов")
async def get_all_recipes(
        service: RecipeServiceDep,
        pagination: PaginationParams = Depends(),
        filters: RecipeFilters = Depends()

):
    return await service.get_paginated(pagination, filters)


@router.get("/top-rated",
            status_code=status.HTTP_200_OK,
            summary="Топ рецептов")
async def get_top_rated_recipes(
        service: RecipeServiceDep,
        limit: int = Query(default=10, ge=1, le=50),
        filters: RecipeFilters = Depends(),

) -> list[RecipeDetail]:
    filters.sort_by = "rating"
    filters.sort_direction = "desc"
    pagination = PaginationParams(page=1, size=limit)
    page = await service.get_paginated(pagination, filters)
    return page.items

@router.get("/top", response_model=list[RecipeDetail], summary="ТОП")
async def get_top_rated_recipes(
    service: RecipeServiceDep,
    limit: int = Query(default=10, ge=1, le=50),
) -> list[RecipeDetail]:
    return await service.get_top_rated(limit=limit)


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
