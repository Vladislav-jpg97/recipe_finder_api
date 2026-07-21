from fastapi import APIRouter
from starlette import status

from backend.dependencies.reviews import RecipeReviewServiceDep

router = APIRouter(
    tags=["Reviews"],
)


@router.get("/recipes/{recipe_id}/reviews", status_code=status.HTTP_200_OK, summary="Обзор рецептов")
async def get_recipe_reviews(recipe_id: int, service: RecipeReviewServiceDep):
    return await service.get_by_recipe(recipe_id)


@router.post("/recipes/{recipe_id}/reviews", status_code=status.HTTP_201_CREATED, summary="Создание обзора")
async def create_recipe_reviews(recipe_id: int, author_name: str, rating: int, content: str,
                                service: RecipeReviewServiceDep):
    return await service.create(recipe_id, author_name, rating, content)


@router.delete("/reviews/{review_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Удаление обзора")
async def delete_reviews(review_id: int, service: RecipeReviewServiceDep):
    return await service.delete(review_id)
