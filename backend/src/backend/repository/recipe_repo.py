from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.models import Recipe


from sqlalchemy import select, func

from backend.schemas.pagination import PaginationParams, Page
from backend.schemas.recipes import RecipeFilters


class RecipeRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> list[Recipe]:
        stmt = select(Recipe).order_by(Recipe.title)
        result = await self.session.execute(stmt)
        recipes = result.scalars().all()
        return list(recipes)

    async def get_by_id(self, recipe_id: int) -> Recipe | None:
        stmt = select(Recipe).where(Recipe.id == recipe_id)
        result = await self.session.execute(stmt)
        return result.scalars().one_or_none()

    async def get_by_slug(self, slug: str) -> Recipe | None:
        stmt = select(Recipe).where(Recipe.slug == slug)
        result = await self.session.execute(stmt)
        return result.scalars().one_or_none()

    async def add(self, recipe: Recipe) -> Recipe:
        self.session.add(recipe)
        await self.session.flush()
        await self.session.refresh(recipe)
        return recipe

    async def delete(self, recipe: Recipe) -> None:
        await self.session.delete(recipe)
        await self.session.flush()

    async def get_paginated(
            self,
            pagination: PaginationParams,
            filters: RecipeFilters
    ):
        query = select(Recipe).options(
            selectinload(Recipe.cuisine),
            selectinload(Recipe.ingredients)
        )

        if filters.search:
            query = query.where(Recipe.title.ilike(f"%{filters.search}%"))

        if filters.cuisine_id:
            query = query.where(Recipe.cuisine_id == filters.cuisine_id)

        if filters.is_vegetarian:
            query = query.where(Recipe.is_vegetarian == filters.is_vegetarian)

        if filters.difficulty:
            query = query.where(Recipe.difficulty == filters.difficulty)

        if filters.max_cooking_time:
            query = query.where(Recipe.cooking_time <= filters.max_cooking_time)

        count_query = select(func.count()).select_from(query.subquery())
        total = (await self.session.execute(count_query)).scalar_one()

        sort_column = getattr(Recipe,filters.sort_by, Recipe.created_at)
        if filters.sort_order == "desc":
            sort_column = sort_column.desc()
        else:
            sort_column = sort_column.asc()

        query = query.order_by(sort_column)

        stmt = query.offset(pagination.offset).limit(pagination.limit)

        result = await self.session.execute(stmt)
        recipe = result.scalars().all()
        return Page.create(
            total=total,
            items=recipe,
            params=pagination
        )