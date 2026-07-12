from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models import Recipe


class RecipeRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self):
        stmt = select(Recipe).order_by(Recipe.title)
        result = await self.session.execute(stmt)
        recipe = result.scalars().all()
        return recipe

    async def get_by_id(self, id: int) -> Recipe:
        stmt = select(Recipe).where(Recipe.cuisine_id == id)
        result = await self.session.execute(stmt)
        recipe = result.scalars().one_or_none()
        return recipe

    async def get_by_slug(self, slug: str) -> Recipe:
        stmt = select(Recipe).where(Recipe.slug == slug)
        result = await self.session.execute(stmt)
        recipe = result.scalars().one_or_none()
        return recipe

    async def add(self, recipe: Recipe):
        self.session.add(recipe)
        await self.session.flush()
        await self.session.refresh(recipe)
        return recipe

    async def delete(self, recipe: Recipe):
        await self.session.delete(recipe)
        await self.session.flush()
