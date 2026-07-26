from fastapi import APIRouter, Depends, Query
from starlette import status

from backend.dependencies.auth import UserServiceDep
from backend.dependencies.recipe import RecipeServiceDep
from backend.models import User
from backend.schemas.pagination import Page, PaginationParams
from backend.schemas.recipes import RecipeCreate, RecipeUpdate, RecipeDetail, RecipeFilters
from backend.services.user_service import UserService

router = APIRouter(
    prefix="/recipes",
    tags=["recipes"],
)


@router.get("/", status_code=status.HTTP_200_OK, response_model=Page[RecipeDetail], summary="Список рецептов")
async def get_all_recipes(
        service: RecipeServiceDep,
        pagination: PaginationParams = Depends(),
        filters: RecipeFilters = Depends(),
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
@router.post("/", response_model=RecipeCreate, status_code=status.HTTP_201_CREATED)
async def create_recipe(
        data: RecipeCreate,
        recipe_service: RecipeServiceDep,
        current_user: User = Depends(UserService.get_current_user),
        ingredient_ids: list[int] | None = None
):
    return await recipe_service.create(data, author_id=current_user.id, ingredient_ids=ingredient_ids)


@router.patch(
    "/{recipe_id}",
    status_code=status.HTTP_200_OK,
    summary="Обновить рецепт"
)
@router.put("/{recipe_id}", response_model=RecipeCreate)
async def update_recipe(
        recipe_id: int,
        data: RecipeUpdate,
        recipe_service: RecipeServiceDep,
        current_user: User = Depends(UserService.get_current_user),
        ingredient_ids: list[int] | None = None,
):
    return await recipe_service.update(
        recipe_id=recipe_id,
        recipe_update=data,
        user_id=current_user.id,
        ingredient_ids=ingredient_ids
    )


@router.delete(
    "/{recipe_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить рецепт"
)
async def delete_recipe(
        recipe_id: int,
        service: RecipeServiceDep,
        current_user: User = Depends(UserService.get_current_user),
):
    return await service.delete(recipe_id=recipe_id, user_id=current_user.id)
