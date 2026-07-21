from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models import RecipeReview


class RecipeReviewRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_recipe(self, recipe_id: int) -> RecipeReview:
        stmt = select(RecipeReview).where(RecipeReview.recipe_id == recipe_id)
        result = await self.session.execute(stmt)
        recipe = result.scalars().all()
        return recipe

    async def get_by_id(self, review_id):
        stmt = select(RecipeReview).where(RecipeReview.id == review_id)
        result = await self.session.execute(stmt)
        recipe = result.scalars().one()
        return recipe

    async def add(self, recipe: RecipeReview):
        self.session.add(recipe)
        await self.session.flush()
        await self.session.refresh(recipe)
        return recipe

    async def delete(self, recipe: RecipeReview):
        await self.session.delete(recipe)
        await self.session.flush()
