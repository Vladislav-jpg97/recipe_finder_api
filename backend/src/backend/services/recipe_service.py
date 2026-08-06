import json

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from backend.core.cache import CacheService
from backend.core.cache_keys import CacheKeys
from backend.models import Recipe, Cuisine
from backend.repository.ingredient_repo import IngredientRepository
from backend.repository.recipe_repo import RecipeRepository
from backend.schemas.pagination import PaginationParams, Page
from backend.schemas.recipes import RecipeCreate, RecipeUpdate, RecipeFilters, RecipeDetail
from backend.utils.slug import SlugGenerate


class RecipeService:

    def __init__(
            self,
            session: AsyncSession,
            recipe_repo: RecipeRepository,
            ingredient_repo: IngredientRepository,
            cache_service : CacheService,

    ):
        self.ingredient_repo = ingredient_repo
        self.repo = recipe_repo
        self.session = session
        self.cache_service = cache_service

    async def get_all(self) -> list[Recipe]:
        recipe = await self.repo.get_all()
        return recipe

    async def get_or_404(self, recipe_id: int) -> Recipe:
        recipe = await self.repo.get_by_id(recipe_id)
        if not recipe:
            raise HTTPException(status_code=404, detail="Recipe not found")
        return recipe

    async def create(self, recipe: RecipeCreate, author_id: int, ingredient_ids: list[int] | None = None) -> Recipe:
        base_slug = SlugGenerate.generate(recipe.title)
        slug = base_slug
        counter = 1

        while await self.repo.get_by_slug(slug):
            slug = SlugGenerate.add_suffix(base_slug, counter)
            counter += 1

        cuisine_exists = await self.session.get(Cuisine, recipe.cuisine_id)
        if not cuisine_exists:
            raise HTTPException(
                status_code=400,
                detail=f"Кухня с ID {recipe.cuisine_id} не найдена"
            )

        ingredients = []
        if ingredient_ids:
            ingredients = await self.ingredient_repo.get_by_ids(ingredient_ids)

        new_recipe = Recipe(
            title=recipe.title,
            slug=slug,
            cuisine_id=recipe.cuisine_id,
            difficulty=recipe.difficulty,
            cooking_time=recipe.cooking_time,
            is_vegetarian=recipe.is_vegetarian,
            rating=recipe.rating,
            servings=recipe.servings,
            calories_per_serving=recipe.calories_per_serving,
            author_id=author_id,
            ingredients=ingredients,
        )
        created_recipe = await self.repo.add(new_recipe)

        await self.session.commit()

        result_recipe = await self.repo.get_by_id(created_recipe.id)

        await self.cache_service.delete_pattern("recipe:list:*")
        return result_recipe

    async def update(
            self,
            recipe_id: int,
            recipe_update: RecipeUpdate,
            user_id: int,
            ingredient_ids: list[int] | None = None
    ) -> Recipe:
        # Получаем саму модель, а не словарь из кэша
        recipe = await self.repo.get_model_by_id(recipe_id)
        if not recipe:
            raise HTTPException(status_code=404, detail="Recipe not found")

        if recipe.author_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )

        if ingredient_ids is not None:
            ingredients = await self.ingredient_repo.get_by_ids(ingredient_ids)
            recipe.ingredients = ingredients

        update_data = recipe_update.model_dump(exclude_unset=True)

        if "title" in update_data:
            new_title = update_data["title"]
            update_data["slug"] = SlugGenerate.generate(new_title)

        for k, v in update_data.items():
            setattr(recipe, k, v)

        await self.session.commit()

        # После коммита возвращаем актуальные данные через получение по ID (или повторный запрос)
        updated_recipe = await self.repo.get_by_id(recipe_id)

        await self.cache_service.delete(CacheKeys.recipe_detail(recipe_id))
        await self.cache_service.delete_pattern("recipe:list:*")
        return updated_recipe

    async def delete(self, recipe_id: int, user_id: int) -> None:
        # Получаем чистую модель из базы, чтобы были доступны атрибуты
        recipe = await self.repo.get_model_by_id(recipe_id)
        if not recipe:
            raise HTTPException(status_code=404, detail="Recipe not found")

        # Сравниваем напрямую author_id (int) и user_id (int)
        if recipe.author_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )

        await self.session.delete(recipe)
        await self.session.commit()
        await self.cache_service.delete(CacheKeys.recipe_detail(recipe_id))
        await self.cache_service.delete_pattern("recipe:list:*")

    async def get_paginated(
            self,
            pagination: PaginationParams,
            filters: RecipeFilters
    ) -> Page[RecipeDetail]:
        return await self.repo.get_paginated(pagination, filters)

    async def get_top_rated(
            self,
            limit: int
    ) -> list[RecipeDetail]:
        recipes = await self.repo.get_top_rated(limit)
        return [RecipeDetail.model_validate(recipe) for recipe in recipes]
