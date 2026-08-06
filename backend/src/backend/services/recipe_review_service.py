from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models import RecipeReview, Recipe
from backend.repository.review_repo import RecipeReviewRepository


class RecipeReviewService:
    def __init__(self, session: AsyncSession, review_repo: RecipeReviewRepository):
        self.session = session
        self.review_repo = review_repo

    async def get_by_recipe(self, recipe_id: int) -> RecipeReview:
        return await self.review_repo.get_by_recipe(recipe_id)

    async def create(self, recipe_id: int, author_name: str, rating: int, content: str) -> RecipeReview:
        if not (1 <= rating <= 5):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Rating must be between 1 and 5"
            )
        recipe = await self.session.get(Recipe, recipe_id)
        if not recipe:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Recipe not found"
            )

        recipe_review = RecipeReview(
            recipe_id=recipe_id,
            author_name=author_name,
            rating=rating,
            content=content
        )
        await self.review_repo.add(recipe_review)
        await self.session.commit()
        await self.session.refresh(recipe_review)
        return recipe_review

    async def delete(self, review_id: int) -> None:
        review = await self.review_repo.get_by_id(review_id)
        if not review:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Review not found"
            )

        await self.review_repo.delete(review)
        await self.session.commit()