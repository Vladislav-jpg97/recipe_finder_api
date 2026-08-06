from typing import Annotated

from fastapi import Depends

from backend.dependencies.database import SessionDep
from backend.repository.ingredient_repo import IngredientRepository
from backend.repository.review_repo import RecipeReviewRepository
from backend.services.recipe_review_service import RecipeReviewService


async def get_review_repo(
        session: SessionDep
):
    return RecipeReviewRepository(session)


ReviewRepoDep = Annotated[
    RecipeReviewRepository,
    Depends(get_review_repo)
]


async def get_review_service(
        session: SessionDep,
        review_repo: ReviewRepoDep
):
    return RecipeReviewService(session=session, review_repo=review_repo)

RecipeReviewServiceDep = Annotated[
    RecipeReviewService,
    Depends(get_review_service)
]
