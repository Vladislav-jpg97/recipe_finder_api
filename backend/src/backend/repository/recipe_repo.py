from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models import Recipe


from sqlalchemy import select

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