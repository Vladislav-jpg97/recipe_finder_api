

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models import Ingredient, ingredient


class IngredientRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> list[Ingredient]:
        stmt = select(Ingredient).order_by(Ingredient.name)
        result = await self.session.execute(stmt)
        recipe = result.scalars().all()
        return list(recipe)

    async def get_by_id(self, ingredient_id: int) -> Ingredient:
        stmt = select(Ingredient).where(Ingredient.id == ingredient_id)
        result = await self.session.execute(stmt)
        recipe = result.scalars().one()
        return recipe

    async def get_by_slug(self, ingredient_slug: str) -> Ingredient:
        stmt = select(Ingredient).where(Ingredient.slug == ingredient_slug)
        result = await self.session.execute(stmt)
        recipe = result.scalars().one_or_none()
        return recipe

    async def get_by_ids(self, ingredient_ids: list[int]) -> list[Ingredient]:
        stmt = select(Ingredient).where(Ingredient.id.in_(ingredient_ids))
        result = await self.session.execute(stmt)
        recipes = result.scalars().all()
        return list(recipes)

    async def add(self, ingredient: Ingredient) -> Ingredient:
        self.session.add(ingredient)
        await self.session.flush()
        await self.session.refresh(ingredient)
        return ingredient

    async def delete(self, ingredient: Ingredient) -> None:
        await self.session.delete(ingredient)
        await self.session.flush()
